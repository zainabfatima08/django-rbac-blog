from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'topic', 'status', 'created_at']
    list_filter = ['author', 'topic']
    search_fields =['topic', 'article']
    list_editable = ['status']
    ordering = ['-created_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author','post','created_at']
    list_filter = ['author', 'post']
    search_fields = ['text']
    ordering = ['-created_at']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
    list_filter = ['post']




