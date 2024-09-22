from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.apartments.models.ratings import Rating
from apps.bookings.models.bookings import Booking


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'advertisement_id', 'rating', 'review', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        user = self.context['request'].user
        advertisement_id = self.context['advertisement_id']  # Получаем ID объявления из контекста

        # Проверяем, есть ли завершенное бронирование
        try:
            booking = Booking.objects.get(
                user=user,
                advertisement_id=advertisement_id,
                is_completed=True
            )
        except Booking.DoesNotExist:
            raise ValidationError('You can only leave a rating or review after the booking is completed.')

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        advertisement_id = self.context['advertisement_id']

        # Получаем бронирование
        booking = Booking.objects.get(
            user=user,
            advertisement_id=advertisement_id,
            is_completed=True
        )

        # Создаем рейтинг с привязкой к бронированию
        rating = Rating.objects.create(
            user=user,
            advertisement_id=advertisement_id,
            booking=booking,
            **validated_data
        )
        return rating
