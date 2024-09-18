from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.serializers.apartment_serializers import AdvertisementSerializer
from apps.apartments.models.view_advertisement import AdvertisementView


class AdvertisementListCreateView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Представление для просмотра конкретного объявления
class AdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.filter(is_active=True)
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        # Вызов стандартного метода получения объявления
        response = super().retrieve(request, *args, **kwargs)

        # Увеличение счетчика просмотров
        advertisement = self.get_object()
        advertisement.view_count = F('view_count') + 1
        advertisement.save()

        # Сохранение просмотра, если пользователь авторизован
        if request.user.is_authenticated:
            advertisement = self.get_object()
            AdvertisementView.objects.create(user=request.user, advertisement=advertisement)

        return response
