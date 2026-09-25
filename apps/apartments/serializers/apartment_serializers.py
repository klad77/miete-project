from rest_framework import serializers
from apps.apartments.models import Advertisement
from apps.users.models.user import User
from drf_spectacular.utils import extend_schema_field

class AdvertisementSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = '__all__'

    @extend_schema_field(
        serializers.FloatField(allow_null=True)
    )

    def get_average_rating(self, obj):
        return obj.average_rating()
