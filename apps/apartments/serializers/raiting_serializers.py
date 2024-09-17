from rest_framework import serializers
from apps.apartments.models.ratings import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'advertisement', 'rating', 'review', 'created_at']
        read_only_fields = ['user', 'advertisement', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value
