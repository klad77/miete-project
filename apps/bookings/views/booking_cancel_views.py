from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from apps.bookings.serializers.booking_serializers import BookingSerializer
from rest_framework import status


class CancelBookingView(generics.UpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        try:
            booking.cancel_booking()
            return Response({'status': 'Booking canceled successfully'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
