from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


@login_required
def mark_notification_read(request, id):
    notif = get_object_or_404(Notification, id=id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'status': 'ok'})


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
def delete_notification(request, id):
    Notification.objects.filter(id=id, user=request.user).delete()
    return JsonResponse({'status': 'deleted'})


@login_required
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'cleared'})



