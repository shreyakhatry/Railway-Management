# Generated by Django 4.2.3 on 2023-07-09 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('station_name', models.CharField(default='', max_length=40)),
                ('station_code', models.CharField(default='', max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Stations',
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_number', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('train_name', models.CharField(max_length=30)),
                ('first_ac', models.IntegerField(default=10)),
                ('second_ac', models.IntegerField(default=10)),
                ('third_ac', models.IntegerField(default=10)),
                ('sleeper', models.IntegerField(default=10)),
                ('days_availability', models.CharField(max_length=15)),
                ('train_destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end', to='dataaccess.station')),
                ('train_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start', to='dataaccess.station')),
            ],
            options={
                'verbose_name_plural': 'Trains',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('seatclass', models.CharField(default='Sl', max_length=5)),
                ('doj', models.DateField()),
                ('boarding_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataaccess.station')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('train', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataaccess.train')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('arrival', models.TimeField()),
                ('departure', models.TimeField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='dataaccess.station')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='dataaccess.station')),
                ('train', models.ManyToManyField(to='dataaccess.train')),
            ],
            options={
                'verbose_name_plural': 'Routes',
            },
        ),
    ]
