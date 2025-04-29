from django.db import models


class Notification(models.Model):
    user = models.UUIDField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "notification"

    def __str__(self):
        return f"Message pour {self.user}, intitule {self.title}"
