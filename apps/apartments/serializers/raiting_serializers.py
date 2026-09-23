from rest_framework import serializers

from apps.apartments.models.ratings import Rating
from apps.bookings.models import Booking


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = [
            'id',
            'user',
            'advertisement',
            'booking',
            'rating',
            'review',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'advertisement',
            'booking',
            'created_at',
        ]

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Rating must be between 1 and 10."
            )

        return value

    def validate(self, data):
        user = self.context['request'].user
        advertisement_id = self.context['advertisement_id']

        booking = Booking.objects.filter(
            user=user,
            advertisement_id=advertisement_id,
            is_completed=True,
            rating__isnull=True,
        ).first()

        if booking is None:
            raise serializers.ValidationError(
                "You can only leave a rating after a completed booking "
                "that has not already been rated."
            )

        self.completed_booking = booking

        return data

    def create(self, validated_data):
        return Rating.objects.create(
            user=self.context['request'].user,
            advertisement_id=self.context['advertisement_id'],
            booking=self.completed_booking,
            **validated_data,
        )
