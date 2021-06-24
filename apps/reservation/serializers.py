from django.contrib.auth.models import User

from rest_framework import serializers

from reservation.models import Reservation
from reservation.models import Room


class ReservationSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')

    class Meta:
        model = Reservation
        fields = '__all__'

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    reservations = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='reservation-detail',
        read_only=True,
    )

    class Meta:
        model = Room
        fields = ('id', 'title', 'description', 'reservations')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    reservations = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='reservation-detail',
        read_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'owned_reservations', 'reservations')
