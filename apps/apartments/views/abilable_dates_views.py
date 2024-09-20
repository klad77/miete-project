from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from datetime import timedelta
from apps.apartments.models.advertisements import Advertisement


class AvailableDatesView(generics.RetrieveAPIView):
    """
    Представление для получения доступных дат для бронирования
    по конкретному объявлению.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Advertisement.objects.all()

    def get(self, request, *args, **kwargs):
        advertisement = self.get_object()  # Получаем объявление по id из URL
        available_dates = advertisement.get_available_dates()  # Вызываем метод для получения свободных дат
        return Response({"available_dates": available_dates})
