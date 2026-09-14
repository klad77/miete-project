from rest_framework import serializers
from apps.apartments.models import Advertisement


class AvailableDatesSerializer(serializers.Serializer):
    dates = serializers.ListField(child=serializers.DateField())

    def to_representation(self, instance):
        # available_dates = instance.get_available_dates()

        return {'dates': instance.get_available_dates()}
