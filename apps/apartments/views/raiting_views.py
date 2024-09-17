from rest_framework import generics
from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer


class AdvertisementReviewListView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        advertisement_id = self.kwargs['advertisement_id']
        return Rating.objects.filter(advertisement__id=advertisement_id)
