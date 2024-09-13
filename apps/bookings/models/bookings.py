from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.apartments.models import Advertisement


class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.advertisement.title} from {self.start_date} to {self.end_date}"
