from django.conf import settings
from django.db import models
from apps.apartments.models import Advertisement


class AdvertisementView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='views')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} viewed {self.advertisement.title} on {self.viewed_at}'
