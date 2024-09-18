from rest_framework import serializers
from django.utils import timezone
from apps.bookings.models import Booking
from apps.apartments.serializers.apartment_serializers import AdvertisementSerializer


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    advertisement = AdvertisementSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'advertisement', 'start_date', 'end_date']


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'advertisement', 'start_date', 'end_date']  # Поля, которые передаются при создании бронирования

    def validate(self, data):
        """
        Проверка, чтобы даты были корректны.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Проверка, чтобы дата начала бронирования была не в прошлом
        if start_date < timezone.now().date():
            raise serializers.ValidationError("Дата начала бронирования не может быть в прошлом.")

        # Проверка, чтобы дата окончания была позже даты начала
        if end_date <= start_date:
            raise serializers.ValidationError("Дата окончания должна быть позже даты начала бронирования.")

        return data

    def create(self, validated_data):
        """
        Создание объекта бронирования с автоматической проверкой статуса
        """
        booking = Booking.objects.create(**validated_data)
        booking.check_booking_status()  # Вызов метода для проверки и установки статуса
        return booking
