from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.serializers.apartment_serializers import AdvertisementSerializer


class AdvertisementListCreateView(generics.ListCreateAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Представление для просмотра конкретного объявления
class AdvertisementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
