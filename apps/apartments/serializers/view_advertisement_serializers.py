from rest_framework import serializers
from apps.apartments.models.view_advertisement import AdvertisementView


class AdvertisementViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementView
        fields = ['advertisement', 'viewed_at']
