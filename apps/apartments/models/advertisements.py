from django.db import models
from apps.users.models.user import User
from apps.apartments.choices.properties import Properties


class Advertisement(models.Model):
    owner = models.ForeignKey(User, related_name='advertisements', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=10)
    rooms = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    properties = models.CharField(
        max_length=15,
        choices=Properties.choices,
        default=Properties.ROOM
    )

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return None

    def __str__(self):
        return f"{self.title}, просмотры: {self.view_count}"
