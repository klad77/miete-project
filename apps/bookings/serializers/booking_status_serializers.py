from rest_framework import serializers
from apps.bookings.models import Booking
from apps.apartments.models import Advertisement
from django.conf import settings


class BookingStatusSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Вывод имени пользователя
    advertisement = serializers.StringRelatedField()  # Вывод названия объявления
    start_date = serializers.DateField(read_only=True)  # Только для чтения
    end_date = serializers.DateField(read_only=True)  # Только для чтения
    status = serializers.ChoiceField(choices=Booking.STATUS_CHOICES)  # Поле для изменения статуса

    class Meta:
        model = Booking
        fields = ['user', 'advertisement', 'start_date', 'end_date', 'status']

class OwnerBookingStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=[
            Booking.CONFIRMED,
            Booking.CANCELED,
        ]
    )

    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        if self.instance.status != Booking.PENDING:
            raise serializers.ValidationError(
                "Only a pending booking can be confirmed or rejected."
            )

        return value
