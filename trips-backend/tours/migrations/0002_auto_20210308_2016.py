# Generated by Django 3.1.7 on 2021-03-08 19:16

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tours', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourinstance',
            name='additional_info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='tourinstance',
            name='tour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tours.tour'),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_people', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('confirmed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('tour_instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tours.tourinstance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]