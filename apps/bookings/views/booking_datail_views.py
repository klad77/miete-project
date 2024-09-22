from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from apps.bookings.models import Booking
from apps.bookings.serializers.booking_status_serializers import BookingStatusSerializer


class BookingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает бронирование с указанным ID для текущего пользователя.
        """
        return Booking.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        """
        Обрабатывает обновление статуса бронирования.
        """
        booking = self.get_object()

        # Проверка и обновление статуса бронирования
        try:
            if 'status' in request.data:
                new_status = request.data['status']

                # Логика для обработки изменения статуса может быть расширена здесь
                booking.status = new_status
                booking.save()

            # Передаем данные в сериализатор для частичного обновления
            serializer = self.get_serializer(booking, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
