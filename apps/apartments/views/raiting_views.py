from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer
from apps.apartments.models.advertisements import Advertisement


class AdvertisementReviewListView(generics.ListAPIView):
    """
    Представление для получения отзывов
    по конкретному объявлению.
    """
    serializer_class = RatingSerializer
    lookup_url_kwarg = 'advertisement_id'

    def get_queryset(self):
        advertisement_id = self.kwargs['advertisement_id']
        return Rating.objects.filter(advertisement__id=advertisement_id)


class AdvertisementReviewCreateView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['advertisement_id'] = self.kwargs['advertisement_id']  # Передача advertisement_id в контекст
        return context

    def perform_create(self, serializer):
        advertisement_id = self.kwargs['advertisement_id']
        advertisement = Advertisement.objects.get(id=advertisement_id)
        serializer.save(user=self.request.user, advertisement=advertisement)
