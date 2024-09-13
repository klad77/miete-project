from rest_framework import serializers
from apps.apartments.models import Advertisement
from apps.users.models.user import User


class AdvertisementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'price_per_night', 'created_at', 'owner', 'rooms']
