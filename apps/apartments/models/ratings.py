from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from apps.apartments.models.advertisements import Advertisement


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()  # Целое число от 1 до 10
    review = models.TextField(blank=True)  # Отзыв (может быть пустым)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'advertisement')  # Один пользователь может оставить только один отзыв на объявление
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating {self.rating} by {self.user} for {self.advertisement.title}"

    def clean(self):
        if self.rating < 1 or self.rating > 10:
            raise ValidationError('Rating must be between 1 and 10.')
