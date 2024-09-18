from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.apartments.models.advertisements import Advertisement
from apps.bookings.models.bookings import Booking


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='ratings')
    booking = models.OneToOneField('bookings.Booking', on_delete=models.CASCADE, related_name='rating', null=True, blank=True)
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    review = models.TextField(blank=True)  # Отзыв (может быть пустым)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating {self.rating} by {self.user} for {self.advertisement}"

    # def clean(self):
    #     if self.rating < 1 or self.rating > 10:
    #         raise ValidationError('Rating must be between 1 and 10.')
