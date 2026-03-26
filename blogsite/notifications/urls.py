from django.urls import path
from . import views

urlpatterns = [
    path('read/<int:id>/', views.mark_notification_read),
    path('read-all/', views.mark_all_notifications_read),
    path('delete/<int:id>/', views.delete_notification),
    path('clear/', views.clear_notifications),

]