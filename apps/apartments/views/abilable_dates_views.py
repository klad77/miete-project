from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.apartments.models.advertisements import Advertisement
from apps.apartments.serializers.available_dates_serializers import (
    AvailableDatesSerializer,
)


class AvailableDatesView(generics.RetrieveAPIView):
    """
    Повертає доступні для бронювання дати конкретного оголошення.
    """

    serializer_class = AvailableDatesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Advertisement.objects.all()
    lookup_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        advertisement = self.get_object()
        available_dates = advertisement.get_available_dates()

        return Response({
            'available_dates': available_dates,
        })
