from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path(
        'schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),
    path(
        'swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    path('users/', include('apps.users.urls')),
    path('apartments/', include('apps.apartments.urls')),
    path('bookings/', include('apps.bookings.urls')),
]
