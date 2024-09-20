from django.db import models
from django.utils import timezone
from datetime import timedelta
from apps.users.models.user import User
from apps.apartments.choices.properties import Properties
# from apps.bookings.models.bookings import Booking


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

    def get_available_dates(self):
        """
        Возвращает список доступных для бронирования дат на следующие 3 месяца.
        """
        current_date = timezone.now().date()

        # Получаем все бронирования для данного объявления
        bookings = self.bookings.filter(end_date__gte=current_date)  # Используем self для доступа к текущему объявлению

        # Список доступных дат
        available_dates = []

        # Цикл на 3 месяца вперед (90 дней)
        for i in range(90):
            date = current_date + timedelta(days=i)

            # Проверяем, что дата не занята
            if not bookings.filter(start_date__lte=date, end_date__gte=date).exists():
                available_dates.append(date)

        return available_dates

    def __str__(self):
        return f"{self.title}"
        # return f"{self.title}, просмотры: {self.view_count}"
