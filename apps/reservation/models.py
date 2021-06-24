from django.db import models


class Room(models.Model):
    title = models.CharField(max_length=127, blank=True, default='')
    description = models.TextField(blank=True, default='')

class Reservation(models.Model):
    title = models.CharField(max_length=127, blank=True, default='')
    start = models.DateTimeField()
    end = models.DateTimeField()
    room = models.ForeignKey(
        Room,
        related_name='reservations',
        on_delete=models.CASCADE,
    )
    organizer = models.ForeignKey(
        'auth.User',
        blank=True,
        related_name='owned_reservations',
        on_delete=models.CASCADE,
    )
    employees = models.ManyToManyField(
        'auth.User',
        blank=True,
        related_name='reservations'
    )

    class Meta:
        ordering = ('room', 'start')
