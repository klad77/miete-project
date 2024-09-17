from rest_framework import generics
from django.db.models import Count
from rest_framework.response import Response
from apps.apartments.models.search_history import SearchHistory
from apps.apartments.serializers.search_history_serializers import *


class SearchHistoryListView(generics.ListAPIView):
    serializer_class = SearchHistorySerializer

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by('-searched_at')


class PopularSearchView(generics.ListAPIView):
    serializer_class = PopularSearchSerializer

    def get_queryset(self):
        # Группировка по ключевым словам и подсчет количества запросов
        return SearchHistory.objects.values('search_term').annotate(count=Count('search_term')).order_by('-count')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
