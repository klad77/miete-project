from django.urls import path
from apps.bookings.views.booking_views import *


urlpatterns = [
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('user-bookings/', UserBookingListView.as_view(), name='user-bookings'),
]
