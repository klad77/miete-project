from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.bookings.models.bookings import Booking
from apps.bookings.serializers.booking_serializers import *


class BookingCreateView(generics.CreateAPIView):
    serializer_class = CreateBookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Представление для просмотра всех бронирований пользователя
class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
