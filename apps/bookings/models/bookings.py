from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from django.conf import settings
from apps.apartments.models import Advertisement
from django.utils import timezone
from django.core.exceptions import ValidationError


class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELED = 'canceled'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed')
    ]

    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    is_completed = models.BooleanField(default=False)  # Флаг завершенного бронирования
    booking_date = models.DateTimeField(auto_now_add=True)

    def check_booking_status(self):
        """
        Проверяет, истекло ли бронирование, и обновляет статус is_completed.
        """
        if self.end_date <= timezone.now().date() and self.status == self.CONFIRMED:
            self.is_completed = True
            self.status = self.COMPLETED
            self.save()  # Сохраняем изменения в базе данных
        return self.is_completed

    def cancel_booking(self):
        """
        Отмена бронирования, если до начала бронирования больше 2 дней.
        """
        days_until_start = (self.start_date - timezone.now().date()).days
        if days_until_start > 2:
            self.status = self.CANCELED
            self.save()
        else:
            raise ValidationError("You can only cancel booking 2 days before start.")

    def save(self, *args, **kwargs):
        # Автоматическая проверка даты окончания перед сохранением объекта
        self.check_booking_status()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking by {self.user} for {self.advertisement} from {self.start_date} to {self.end_date}"
