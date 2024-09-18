from django.contrib import admin
from apps.apartments.models.advertisements import Advertisement
from apps.apartments.models.ratings import Rating
from apps.apartments.models.search_history import SearchHistory
from apps.apartments.models.view_advertisement import AdvertisementView

admin.site.register(Advertisement)
admin.site.register(Rating)
admin.site.register(SearchHistory)
admin.site.register(AdvertisementView)
