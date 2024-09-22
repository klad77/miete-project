from django.urls import path
from apps.bookings.views.booking_views import *
from apps.bookings.views.booking_cancel_views import *
from apps.bookings.views.booking_owner_views import *
from apps.bookings.views.booking_status_views import *
from apps.bookings.views.booking_user_views import *
from apps.bookings.views.booking_datail_views import BookingDetailView


urlpatterns = [
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('user-bookings/', UserBookingListView.as_view(), name='user-bookings'),
    path('bookings/owner/', OwnerBookingListView.as_view(), name='owner-bookings'),
    path('bookings/user/', UserBookingListView.as_view(), name='user-bookings'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
]
