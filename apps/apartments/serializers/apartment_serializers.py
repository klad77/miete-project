from rest_framework import serializers
from apps.apartments.models import Advertisement
from apps.users.models.user import User


class AdvertisementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'
        # fields = ['id', 'title', 'description', 'price_per_night', 'created_at', 'owner', 'rooms']

    def get_average_rating(self, obj):
        return obj.average_rating()
