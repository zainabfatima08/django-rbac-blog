from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.

class Post(models.Model):

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]
    topic = models.CharField(max_length = 170)
    article = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    status = models.CharField(max_length = 10, choices= STATUS_CHOICES, default = 'Draft')
    slug = models.SlugField(max_length = 200, unique = True , blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    
    def save(self, *args, **kwargs):
        if not self.slug:                          # sirf pehli baar banao
            self.slug = slugify(self.topic)        # topic se slug banao
            # Agar same slug exist kare toh unique banao
            original_slug = self.slug
            counter = 1
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.author.username} on {self.post.topic}"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = 'likes')

    class Meta:
        unique_together=['user', 'post']

    def __str__(self):
        return f"{self.user.username} liked '{self.post.topic}'"