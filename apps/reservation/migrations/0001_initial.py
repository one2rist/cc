# Generated by Django 3.2.4 on 2021-06-24 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=127)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=127)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('employees', models.ManyToManyField(blank=True,
                 related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE,
                 related_name='owned_reservations', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='reservations', to='reservation.room')),
            ],
        ),
    ]
