from rest_framework import generics, permissions

from apps.bookings.models import Booking
from apps.bookings.serializers.booking_status_serializers import (
    BookingStatusSerializer,
)


class BookingDetailView(generics.RetrieveAPIView):
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        return Booking.objects.filter(user=self.request.user)
