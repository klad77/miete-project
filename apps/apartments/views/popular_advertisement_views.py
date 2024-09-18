from rest_framework import generics
from apps.apartments.models import Advertisement
from apps.apartments.serializers.apartment_serializers import AdvertisementSerializer


class PopularAdvertisementsView(generics.ListAPIView):
    serializer_class = AdvertisementSerializer
    queryset = Advertisement.objects.filter(is_active=True).order_by('-view_count')
