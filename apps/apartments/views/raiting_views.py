from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer


class RatingListView(generics.ListAPIView):
    """
    Повертає рейтинги та відгуки для конкретного оголошення.
    """

    serializer_class = RatingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rating.objects.none()

        advertisement_id = self.kwargs.get('advertisement_id')

        if advertisement_id is None:
            return Rating.objects.none()

        return Rating.objects.filter(
            advertisement_id=advertisement_id,
        ).select_related(
            'advertisement',
            'user',
            'booking',
        )


class CreateRatingView(generics.CreateAPIView):
    """
    Створює рейтинг після завершеного бронювання.
    """

    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['advertisement_id'] = self.kwargs['advertisement_id']
        return context
