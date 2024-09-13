from rest_framework import serializers
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
        fields = ['advertisement', 'start_date', 'end_date']
