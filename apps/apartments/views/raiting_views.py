from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.apartments.models.ratings import Rating
from apps.apartments.serializers.raiting_serializers import RatingSerializer
from apps.apartments.models.advertisements import Advertisement


class AdvertisementReviewListView(generics.ListAPIView):
    serializer_class = RatingSerializer

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

# class AdvertisementReviewCreateView(generics.CreateAPIView):
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#
#         # Проверка на наличие advertisement_id в kwargs
#         advertisement_id = self.kwargs.get('advertisement_id')
#         if advertisement_id is None:
#             raise ValidationError('Advertisement ID not provided in the request.')
#
#         context['advertisement_id'] = advertisement_id
#         return context
#
#     def perform_create(self, serializer):
#         advertisement_id = self.kwargs.get('advertisement_id')
#         if advertisement_id is None:
#             raise ValidationError('Advertisement ID not provided in the request.')
#
#         advertisement = Advertisement.objects.get(id=advertisement_id)
#         serializer.save(user=self.request.user, advertisement=advertisement)

# class AdvertisementReviewCreateView(generics.CreateAPIView):
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#
#         # Проверка на наличие advertisement_id
#         advertisement_id = self.kwargs.get('advertisement_id')
#         if advertisement_id is None:
#             raise ValidationError('Advertisement ID not provided in the request.')
#
#         # Логирование для отладки
#         print(f"Advertisement ID: {advertisement_id}")
#
#         context['advertisement_id'] = advertisement_id
#         return context
#
#     def perform_create(self, serializer):
#         advertisement_id = self.kwargs.get('advertisement_id')
#         if advertisement_id is None:
#             raise ValidationError('Advertisement ID not provided in the request.')
#
#         advertisement = Advertisement.objects.get(id=advertisement_id)
#         serializer.save(user=self.request.user, advertisement=advertisement)
#

# class AdvertisementReviewCreateView(generics.CreateAPIView):
#     serializer_class = RatingSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#
#         advertisement_id = self.kwargs.get('advertisement_id')
#         if advertisement_id is None:
#             raise ValidationError('Advertisement ID not provided in the request.')
#
#         context['advertisement_id'] = advertisement_id
#         return context
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

