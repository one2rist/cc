from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from reservation import views

urlpatterns = [
    path('', views.home),

    path(
        'reservations/',
        views.ReservationList.as_view(),
        name='reservations',
    ),
    path(
        'reservations/<int:pk>/',
        views.ReservationDetail.as_view(),
        name='reservation-detail',
    ),
    path(
        'users/',
        views.UserList.as_view(),
        name='users',
    ),
    path(
        'users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user',
    ),
    path(
        'rooms/',
        views.RoomList.as_view(),
        name='rooms',
    ),
    path(
        'rooms/<int:pk>/',
        views.RoomDetail.as_view(),
        name='room',
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
