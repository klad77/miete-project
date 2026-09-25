from rest_framework import generics, permissions

from apps.bookings.models import Booking
from apps.bookings.serializers.booking_serializers import BookingSerializer


class OwnerBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status']

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        return Booking.objects.filter(
            advertisement__owner=self.request.user,
        )
