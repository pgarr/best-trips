# Generated by Django 3.1.7 on 2021-03-02 19:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('max_participants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('short_description', models.CharField(max_length=200)),
                ('long_description', models.TextField()),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('created', models.DateTimeField(auto_now=True)),
                ('modified', models.DateTimeField(auto_now_add=True)),
                ('departure_country', models.CharField(max_length=200)),
                ('departure_city', models.CharField(max_length=200)),
                ('duration_days', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='TourInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.DateTimeField()),
                ('return_time', models.DateTimeField()),
                ('additional_info', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.tour')),
            ],
        ),
    ]
