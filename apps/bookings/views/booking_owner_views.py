from rest_framework import generics, permissions

from apps.bookings.models import Booking
from apps.bookings.serializers.booking_status_serializers import (
    OwnerBookingStatusSerializer,
)


class OwnerBookingStatusView(generics.UpdateAPIView):
    serializer_class = OwnerBookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch', 'options']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        return Booking.objects.filter(
            advertisement__owner=self.request.user,
        )
