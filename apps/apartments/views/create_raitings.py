from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer


class CreateRatingView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['advertisement_id'] = self.kwargs['advertisement_id']  # Передаем ID объявления в контекст
        return context

    def perform_create(self, serializer):
        advertisement_id = self.kwargs['advertisement_id']
        advertisement = Advertisement.objects.get(id=advertisement_id)
        serializer.save(user=self.request.user, advertisement=advertisement)
