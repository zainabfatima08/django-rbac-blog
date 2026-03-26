from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification


class NotificationCreator:

    def __init__(self):
        self.channel_layer = get_channel_layer()

    # NEW POST
    def post_created(self, users, post):
        for user in users:
            notif = Notification.objects.create(
                user=user,
                post=post,
                message=f'New post published: "{post.topic}"',
                notif_type='new_post'
            )
            self._send_ws(user.id, notif)

    # COMMENT
    def comment_created(self, post_author, post, commenter):
        notif = Notification.objects.create(
            user=post_author,
            post=post,
            message=f'{commenter.username} commented on "{post.topic}"',
            notif_type='comment'
        )

        print("📡 SENDING TO GROUP:", f"notifications_{commenter.id}")
        self._send_ws(post_author.id, notif)

    # LIKE

    def like_created(self, post_author, post, liker):
        notif = Notification.objects.create(
            user=post_author,
            post=post,
            message=f'{liker.username} liked "{post.topic}"',
            notif_type='like'
        )

        print("📡 SENDING TO GROUP:", f"notifications_{liker.id}")
        self._send_ws(post_author.id, notif)

    # WEBSOCKET SEND
    def _send_ws(self, user_id, notif):
        print(" GROUP_SEND CALLED:", f"notifications_{user_id}")

        async_to_sync(self.channel_layer.group_send)(
            f"notifications_{user_id}",
            {
                "type": "send_notification",
                "id": notif.id,
                "message": notif.message,
                "notif_type": notif.notif_type,
                "post_slug": notif.post.slug if notif.post else None,
                "created_at": notif.created_at.strftime("%H:%M")
            }
        )