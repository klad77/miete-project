from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.serializers.apartment_serializers import AdvertisementSerializer
from apps.apartments.utils.filters import AdvertisementFilter


class AdvertisementListSearchView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.filter(is_active=True)  # Показывать только активные объявления
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']  # Поля, по которым будет производиться поиск
    filterset_class = AdvertisementFilter  # Указываем класс фильтров
    ordering_fields = ['price_per_night', 'created_at']  # Поля для сортировки
    ordering = ['-created_at']  # Сортировка по дате создания (новые сверху)
