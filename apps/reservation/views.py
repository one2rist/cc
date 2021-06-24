from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from reservation.models import Reservation
from reservation.models import Room
from reservation.permissions import IsOwnerOrReadOnly, IsSuperOrReadOnly
from reservation.serializers import ReservationSerializer
from reservation.serializers import UserSerializer
from reservation.serializers import RoomSerializer



@api_view(['GET'])
def home(request, format=None):
    return Response({
        'employees': reverse('users', request=request, format=format),
        'reservations': reverse('reservations', request=request, format=format),
        'rooms': reverse('rooms', request=request, format=format),
    })

class ReservationList(generics.ListCreateAPIView):
    """
    List all reservations:
    curl -H "Content-type: application/json" http://127.0.0.1:8000/reservation/
    http http://127.0.0.1:8000/reservation/ Accept:application/json
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def _conflicting(self, data):
        start = data.get('start')
        end = data.get('end')
        room = data.get('room')
        if not (start or end or room):
            raise ValidationError('Room, Start and End must be provided')
        return Reservation.objects.filter(
            start__lt=end,
            end__gt=start,
            room=room,
        ).exists()

    def perform_create(self, serializer):
        if self._conflicting(serializer.validated_data):
            raise ValidationError('This time slot is alredy taken.')
        serializer.save(organizer=self.request.user)

class ReservationDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a reservation.
    Update (PUT):
    http --json PUT http://127.0.0.1:8000/reservation.json title="One more res"
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def _conflicting(self, data):
        instance = self.get_object()
        start = data.get('start', instance.start)
        end = data.get('end', instance.end)
        room = data.get('room', instance.room.pk)
        return Reservation.objects.filter(
            start__lt=end,
            end__gt=start,
            room=room,
        ).exclude(
            pk=instance.pk #remove self
        ).exists()

    def perform_update(self, serializer):
        if self._conflicting(serializer.validated_data):
            raise ValidationError('This time slot is alredy taken.')
        serializer.save()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSuperOrReadOnly]

class RoomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSuperOrReadOnly]
