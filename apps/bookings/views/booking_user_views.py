from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from apps.bookings.serializers.booking_serializers import BookingSerializer
from rest_framework import status


class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Під час створення Swagger-схеми користувач відсутній
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()

        status_filter = self.request.query_params.get('status')

        queryset = Booking.objects.filter(user=self.request.user)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
