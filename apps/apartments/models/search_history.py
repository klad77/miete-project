from django.conf import settings  # Импорт настроек
from django.db import models


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="search_history")
    search_term = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} searched for "{self.search_term}" on {self.searched_at}'
