from django.urls import path, include


urlpatterns = [
    path('users/', include('apps.users.urls')),
    path('apartments/', include('apps.apartments.urls')),
    path('bookings/', include('apps.bookings.urls')),
]
