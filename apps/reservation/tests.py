from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from reservation.models import Room, Reservation


class RoomReservationsTests(APITestCase):
    def setUp(self):
        U1 = {'username': 'admin', 'email': 'a@a.com', 'password': 'abCD12#$'}
        U2 = {'username': 'Joahn', 'email': 'j@a.com', 'password': 'abCD12#$'}
        u1 = User.objects.create(**U1)
        u2 = User.objects.create(**U2)
        R1 = {'title': 'Room 1'}
        R2 = {'title': 'Room 2'}
        r1 = Room.objects.create(**R1)
        r2 = Room.objects.create(**R2)
        B1 = {
            'title': 'Booking 1',
            'room': r1,
            'organizer': u1,
            'start': '2022-01-01T01:00:00Z',
            'end': '2022-01-01T02:00:00Z',
        }
        b1 = Reservation.objects.create(**B1)
        b1.employees.set([u1, u2])

    def test_get_meeting_room_list(self):
        """
        Get meeting rooms list
        """

        # get list of rooms:
        url = reverse('rooms')
        responce = self.client.get(url, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(len(responce.data), 2)
        # print(responce.data)

    def test_get_meeting_room_reservations(self):
        """
        Get meeting room reservations
        """

        # get room 2:
        r1 = Room.objects.get(title='Room 1')
        url = reverse('room', args=(r1.pk,))
        responce = self.client.get(url, format='json')
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(len(responce.data['reservations']), 1)
        # print(responce.data)

    def test_create_reservations(self):
        """
        Create reservation
        Reservation has title, from and to dates, employees
        """

        r1 = Room.objects.get(title='Room 1')
        u1 = User.objects.get(username='admin')
        data = {
            'title': 'Booking 1',
            'room': r1.pk,
            'organizer': u1.pk,
            'start': '2022-01-02T01:00:00Z',
            'end': '2022-01-02T02:00:00Z',
        }

        self.client.force_authenticate(user=u1)
        url = reverse('reservations')

        # posting not overlapping reservation:
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_201_CREATED)

        # posting overlapping reservation:
        # same is in setUp()
        data.update({
            'start': '2022-01-01T01:00:00Z',
            'end': '2022-01-01T02:00:00Z',
        })
        responce = self.client.post(url, data, format='json')
        self.assertEqual(responce.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_reservation(self):
        """
        Cancel reservation
        only organizer can cancel
        """

        u1 = User.objects.get(username='admin')
        u2 = User.objects.get(username='Joahn')
        b1 = Reservation.objects.get(organizer=u1)

        url = reverse('reservation-detail', args=(b1.pk, ))

        # anonymous user gets 403:
        responce = self.client.delete(url, format='json')
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

        # not organizer user gets 403:
        self.client.force_authenticate(user=u2)
        responce = self.client.delete(url, format='json')
        self.assertEqual(responce.status_code, status.HTTP_403_FORBIDDEN)

        # organizer can delete:
        self.client.force_authenticate(user=u1)
        responce = self.client.delete(url, format='json')
        self.assertEqual(responce.status_code, status.HTTP_204_NO_CONTENT)
