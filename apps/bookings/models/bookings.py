from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.apartments.models import Advertisement
from django.utils import timezone


class Booking(models.Model):
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)  # Флаг завершенного бронирования
    booking_date = models.DateTimeField(auto_now_add=True)

    def check_booking_status(self):
        """
        Проверяет, истекло ли бронирование, и обновляет статус is_completed.
        """
        if self.end_date <= timezone.now().date():
            self.is_completed = True
            self.save()  # Сохраняем изменения в базе данных
        return self.is_completed

    def save(self, *args, **kwargs):
        # Автоматическая проверка даты окончания перед сохранением объекта
        self.check_booking_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user} for {self.advertisement} from {self.start_date} to {self.end_date}"
