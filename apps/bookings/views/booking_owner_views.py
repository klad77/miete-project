from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from apps.bookings.serializers.booking_serializers import BookingSerializer
from rest_framework import status


class OwnerBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Фильтрация по объявлениям владельца
        return Booking.objects.filter(advertisement__owner=self.request.user)

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        new_status = request.data.get('status')
        if new_status in [Booking.CONFIRMED, Booking.CANCELED]:
            booking.status = new_status
            booking.save()
            return Response({'status': 'Booking status updated successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
