from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.view_advertisement import AdvertisementView
from apps.apartments.serializers.view_advertisement_serializers import AdvertisementViewSerializer


class AdvertisementViewHistoryView(generics.ListAPIView):
    serializer_class = AdvertisementViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает историю просмотров только для авторизованного пользователя
        return AdvertisementView.objects.filter(user=self.request.user).order_by('-viewed_at')
