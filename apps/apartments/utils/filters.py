import django_filters
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.choices.properties import Properties


class AdvertisementFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price_per_night', lookup_expr='lte')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    min_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='gte')
    max_rooms = django_filters.NumberFilter(field_name='rooms', lookup_expr='lte')
    property_type = django_filters.ChoiceFilter(field_name='properties', choices=Properties.choices)

    class Meta:
        model = Advertisement
        fields = ['min_price', 'max_price', 'city', 'min_rooms', 'max_rooms', 'property_type']
