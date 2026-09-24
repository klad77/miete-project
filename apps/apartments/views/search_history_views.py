from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.apartments.models.search_history import SearchHistory
from apps.apartments.serializers.search_history_serializers import (
    PopularSearchSerializer,
    SearchHistorySerializer,
)


class SearchHistoryListView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return SearchHistory.objects.none()

        return SearchHistory.objects.filter(
            user=self.request.user,
        ).order_by('-searched_at')


class PopularSearchView(generics.ListAPIView):
    serializer_class = PopularSearchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return (
            SearchHistory.objects
            .values('search_term')
            .annotate(count=Count('search_term'))
            .order_by('-count', 'search_term')
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
