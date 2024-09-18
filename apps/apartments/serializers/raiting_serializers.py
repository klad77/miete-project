from rest_framework import serializers
from django.core.exceptions import ValidationError
from apps.apartments.models.ratings import Rating
from apps.bookings.models.bookings import Booking


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'advertisement', 'rating', 'review', 'created_at']
        # read_only_fields = ['user', 'advertisement', 'created_at']
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

        # Создаем отзыв и рейтинг
        rating = Rating.objects.create(
            user=user,
            advertisement_id=advertisement_id,
            booking=booking,  # Связываем отзыв с бронированием
            rating=validated_data['rating'],
            review=validated_data.get('review', '')
        )
        return rating
    # def validate(self, data):
    #     user = self.context['request'].user
    #     booking = data.get('booking')
    #
    #     # Проверка, что бронирование завершено
    #     if not booking.is_completed:
    #         raise serializers.ValidationError("You can only leave a rating or review after the booking is completed.")
    #
    #     # Проверка, что текущий пользователь связан с бронированием
    #     if booking.user != user:
    #         raise serializers.ValidationError("You can only rate your own bookings.")
    #
    #     return data

    # def validate_rating(self, value):
    #     if value < 1 or value > 10:
    #         raise serializers.ValidationError("Rating must be between 1 and 10.")
    #     return value
