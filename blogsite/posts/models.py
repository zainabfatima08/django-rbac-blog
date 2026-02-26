from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
    topic = models.CharField(max_length = 170)
    article = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.topic