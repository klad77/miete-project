from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer


class CreateRatingView(generics.CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        advertisement_id = self.kwargs['advertisement_id']
        advertisement = Advertisement.objects.get(id=advertisement_id)
        serializer.save(user=self.request.user, advertisement=advertisement)
