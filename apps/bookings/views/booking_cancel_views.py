from django.core.exceptions import ValidationError
from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.bookings.models import Booking
from apps.bookings.serializers.booking_status_serializers import BookingStatusSerializer
from rest_framework import status


class CancelBookingView(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает бронирования, которые принадлежат текущему пользователю.
        """
        return Booking.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        booking = self.get_object()
        try:
            booking.cancel_booking()  # Отмена бронирования

            # Проверяем частичные данные (partial=True для частичного обновления)
            serializer = self.get_serializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Сохраняем изменения

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
