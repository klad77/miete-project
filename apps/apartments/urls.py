from django.urls import path
from apps.apartments.views.apartament_views import *
from apps.apartments.views.advertisement_status import *


urlpatterns = [
    path('advertisements/', AdvertisementListCreateView.as_view(), name='advertisements'),
    path('advertisements/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement-detail'),
    path('advertisements/<int:pk>/status/', ToggleAdvertisementStatusView.as_view(), name='advertisement-status'),
]
