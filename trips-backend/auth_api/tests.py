import jwt
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@pytest.mark.django_db
class TestAuthApiRoutes:

    @pytest.fixture
    def sample_user(self, create_user):
        credentials = {'username': 'test',
                       'email': 'test@test.pl',
                       'password': 'Test123#'}
        user = create_user(**credentials)
        return user, credentials

    def test_get_token_success(self, client, sample_user):
        user, credentials = sample_user

        response = client.post(reverse('token_obtain_pair'),
                               {'username': credentials['username'], 'password': credentials['password']})

        assert response.status_code == 200
        assert 'access' in response.json()
        assert 'refresh' in response.json()

    def test_get_token_invalid_credentials(self, client, sample_user):
        user, credentials = sample_user

        response = client.post(reverse('token_obtain_pair'),
                               {'username': credentials['username'], 'password': 'wrongpassword'})

        assert response.status_code == 401
        assert 'access' not in response.json()
        assert 'refresh' not in response.json()

    def test_refresh_token_success(self, client, sample_user):
        user, credentials = sample_user

        refresh = get_tokens_for_user(user)['refresh']

        response = client.post(reverse('token_refresh'),
                               {'refresh': refresh})

        assert response.status_code == 200
        assert 'access' in response.json()
        assert 'refresh' not in response.json()

    def test_refresh_token_failure(self, client, sample_user):
        refresh = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")

        response = client.post(reverse('token_refresh'),
                               {'refresh': refresh})

        assert response.status_code == 401
        assert 'access' not in response.json()
        assert 'refresh' not in response.json()

    def test_register_success(self, client):
        username = 'test123'
        email = 'test123@test.pl'
        password = 'test098$'

        response = client.post(reverse('register'), {'username': username, 'email': email, 'password': password})

        assert response.status_code == 201

    def test_register_failure_occupied_username(self, client, sample_user):
        user, credentials = sample_user

        email = 'test123@test.pl'
        password = 'test098$'

        response = client.post(reverse('register'),
                               {'username': credentials['username'], 'email': email, 'password': password})

        assert response.status_code == 400
        assert 'username' in response.json()

    @pytest.mark.xfail
    def test_register_failure_occupied_email(self, client, sample_user):
        user, credentials = sample_user

        username = 'test123'
        password = 'test098$'

        response = client.post(reverse('register'),
                               {'username': username, 'email': credentials['email'], 'password': password})

        assert response.status_code == 400
        assert 'email' in response.json()

    def test_register_failure_no_data(self, client, sample_user):
        response = client.post(reverse('register'), {})

        assert response.status_code == 400

    def test_register_failure_weak_password(self, client):
        username = 'test123'
        email = 'test123@test.pl'
        password = '1'

        response = client.post(reverse('register'), {'username': username, 'email': email, 'password': password})

        assert response.status_code == 400
        assert 'password' in response.json()

    def test_register_success_not_returns_password(self, client):
        username = 'test123'
        email = 'test123@test.pl'
        password = 'test098$'

        response = client.post(reverse('register'), {'username': username, 'email': email, 'password': password})

        assert response.status_code == 201
        assert 'password' not in response.json()

    def test_register_password_not_saved_in_plain_text(self, client):
        username = 'test123'
        email = 'test123@test.pl'
        password = 'test098$'

        response = client.post(reverse('register'), {'username': username, 'email': email, 'password': password})
        assert response.status_code == 201

        new_user = User.objects.get(username=username)
        assert not new_user.password == password
