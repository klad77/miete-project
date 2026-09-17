from django.urls import path

from apps.bookings.views.booking_views import BookingCreateView
from apps.bookings.views.booking_cancel_views import CancelBookingView
from apps.bookings.views.booking_status_views import OwnerBookingListView
from apps.bookings.views.booking_user_views import UserBookingListView
from apps.bookings.views.booking_datail_views import BookingDetailView
from apps.bookings.views.booking_owner_views import OwnerBookingStatusView


urlpatterns = [
    path(
        'bookings/',
        BookingCreateView.as_view(),
        name='create-booking',
    ),
    path(
        'bookings/owner/',
        OwnerBookingListView.as_view(),
        name='owner-bookings',
    ),
    path(
        'bookings/user/',
        UserBookingListView.as_view(),
        name='user-bookings',
    ),
    path(
        'bookings/<int:pk>/',
        BookingDetailView.as_view(),
        name='booking-detail',
    ),
    path(
        'bookings/<int:pk>/cancel/',
        CancelBookingView.as_view(),
        name='cancel-booking',
    ),
    path(
        'bookings/<int:pk>/owner-status/',
        OwnerBookingStatusView.as_view(),
        name='owner-booking-status',
    ),
]
