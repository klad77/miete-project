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
    properties = models.CharField(
        max_length=15,
        choices=Properties.choices,
        default=Properties.ROOM
    )

    def __str__(self):
        return self.title
        # return f"{self.title} by {self.user.username}"
