from rest_framework import serializers
from apps.apartments.models.search_history import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['search_term', 'searched_at']


class PopularSearchSerializer(serializers.Serializer):
    search_term = serializers.CharField(max_length=255)
    count = serializers.IntegerField()
