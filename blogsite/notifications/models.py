from django.db import models
from django.conf import settings
from posts.models import Post

# Create your models here.

class Notification(models.Model):

    NOTIFICATION_TYPES = [
        ('new_post', 'New Post Published'),
        ('comment', 'New Comment'),
        ('like', 'New Like')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "notifications")
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "notifications")
    message = models.CharField(max_length = 70)
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    notif_type = models.CharField(max_length = 20, choices = NOTIFICATION_TYPES, default = 'new_post')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.message}"
