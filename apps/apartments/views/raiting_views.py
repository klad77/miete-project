from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.apartments.models.advertisement_review import AdvertisementReview
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.serializers.advertisement_review_serializers import (
    AdvertisementReviewSerializer,
)


class AdvertisementReviewListView(generics.ListAPIView):
    """
    Повертає відгуки для конкретного оголошення.
    """

    serializer_class = AdvertisementReviewSerializer

    def get_queryset(self):
        advertisement_id = self.kwargs.get('advertisement_id')

        if getattr(self, 'swagger_fake_view', False):
            return AdvertisementReview.objects.none()

        if advertisement_id is None:
            return AdvertisementReview.objects.none()

        return AdvertisementReview.objects.filter(
            advertisement_id=advertisement_id
        ).select_related('advertisement', 'user')


class AdvertisementReviewCreateView(generics.CreateAPIView):
    """
    Створює відгук для конкретного оголошення.
    """

    serializer_class = AdvertisementReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        advertisement = get_object_or_404(
            Advertisement,
            id=self.kwargs['advertisement_id'],
        )

        serializer.save(
            user=self.request.user,
            advertisement=advertisement,
        )
