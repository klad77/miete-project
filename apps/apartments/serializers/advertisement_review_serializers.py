from rest_framework import serializers
from apps.apartments.models.advertisement_review import AdvertisementReview


class AdvertisementReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementReview
        fields = [
            'id',
            'advertisement',
            'user',
            'review',
            'rating',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'advertisement',
            'user',
            'created_at',
            'updated_at',
        ]