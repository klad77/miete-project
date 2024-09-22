from django.urls import path
from apps.apartments.views.apartament_views import *
from apps.apartments.views.advertisement_status import ToggleAdvertisementStatusView
from apps.apartments.views.apartament_search import AdvertisementListSearchView
from apps.apartments.views.raiting_views import AdvertisementReviewListView, AdvertisementReviewCreateView
from apps.apartments.views.create_raitings import CreateRatingView
from apps.apartments.views.search_history_views import *
from apps.apartments.views.view_advertisement_views import AdvertisementViewHistoryView
from apps.apartments.views.popular_advertisement_views import PopularAdvertisementsView
from apps.apartments.views.abilable_dates_views import AvailableDatesView


urlpatterns = [
    path('advertisements/', AdvertisementListCreateView.as_view(), name='advertisements'),
    path('advertisements/search/', AdvertisementListSearchView.as_view(), name='advertisements-search'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement-detail'),
    path('advertisements/<int:pk>/status/', ToggleAdvertisementStatusView.as_view(), name='advertisement-status'),
    path('advertisements/<int:advertisement_id>/reviews/', AdvertisementReviewListView.as_view(),
         name='advertisement-reviews'),
    path('advertisements/<int:advertisement_id>/add-review/', AdvertisementReviewCreateView.as_view(), name='add-review'),
    # path('advertisements/<int:advertisement_id>/add-review/', CreateRatingView.as_view(), name='add-review'),
    path('search-history/', SearchHistoryListView.as_view(), name='search-history'),
    path('search/popular/', PopularSearchView.as_view(), name='popular-search'),
    path('advertisements/views/', AdvertisementViewHistoryView.as_view(), name='advertisement-view-history'),
    path('advertisements/popular/', PopularAdvertisementsView.as_view(), name='popular-advertisements'),
    path('advertisement/<int:pk>/available-dates/', AvailableDatesView.as_view(), name='available-dates'),
]
