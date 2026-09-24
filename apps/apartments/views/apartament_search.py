from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics

from apps.apartments.models.advertisements import Advertisement
from apps.apartments.models.search_history import SearchHistory
from apps.apartments.serializers.apartment_serializers import (
    AdvertisementSerializer,
)
from apps.apartments.utils.filters import AdvertisementFilter


class AdvertisementListSearchView(generics.ListAPIView):
    """
    Пошук, фільтрація та сортування активних оголошень.
    """

    queryset = Advertisement.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['title', 'description']
    filterset_class = AdvertisementFilter
    ordering_fields = ['price_per_night', 'created_at']
    ordering = ['-created_at']

    def filter_queryset(self, queryset):
        search_term = self.request.query_params.get('search', '').strip()

        if search_term and self.request.user.is_authenticated:
            SearchHistory.objects.create(
                user=self.request.user,
                search_term=search_term,
            )

        return super().filter_queryset(queryset)
