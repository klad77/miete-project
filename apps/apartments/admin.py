from django.contrib import admin
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.models.ratings import Rating
from apps.apartments.models.search_history import SearchHistory

admin.site.register(Advertisement)
admin.site.register(Rating)
admin.site.register(SearchHistory)
