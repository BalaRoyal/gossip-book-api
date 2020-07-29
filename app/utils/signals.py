from django.dispatch import Signal
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

import json

interested_users = Signal(providing_args=['instance', 'user', 'created'])

comment_signal = Signal(providing_args=['post', 'instance',
                                        'user', 'created'
                                        ])
vote_signal = Signal(providing_args=['instance', 'post',
                                     'user', 'created'
                                     ])

follow_user_signal = Signal(providing_args=['instance', 'user',
                                            'created'])

new_message_signal = Signal(providing_args=['instance', 'user',
                                            'receiver', 'created'])


def send_notification(room_name, notification_obj):
    """Send user notification to the specified room name

    Args:
        room_name (str): The channel layer room name
        notification_obj (Notification): Notification model instance.
    """
    channel_layer = get_channel_layer()
    data = json.dumps(NotificationSerializer(notification_obj).data)

    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            'type': 'notification_message',
            'data': data
        }
    )


def send_follow_user_notification(instance, user, created, **kwargs):
    """send notification to a particular user being followed

    Args:
        instance (Model): a follow user model instance
        user (User): user who is following the other user
        created (Boolean): True if the follow instance has been created, False otherwise
    """

    if created:

        room_name = f"notification_{instance.user.id}"

        notification_obj = Notification.objects.create(
            user=instance.user,
            message=f"{user.username} started following you!",
            origin='FOLLOW',
        )

        send_notification(room_name, notification_obj)


def send_message_notification(instance, user, receiver, created, **kwargs):
    """Notify users of new messages being sent to them.

    Args:
        instance (Message): a message instance being sent to the receiver
        sender (User): User who is sending a message
        receiver (User): user who is supposed to receive a message
        created (Boolean): True if a message instance has been created, False otherwise
    """

    if created:
        username = user.username,
        room_name = f"notification_{receiver.id}"

        notification_obj = Notification.objects.create(
            user=receiver,
            message=f"new message from {user.username}",
            origin='MESSAGE')

        send_notification(room_name, notification_obj)


def send_post_vote_notification(post_name, instance, post, user, created, **kwargs):
    """Send notification when a user's gossip or question 
    is liked. this can also be used to send notifications when
     a user comment or answer is liked.

    Args:
        post_name (str): name of the instance being voted. eg: question, gossip
        post (Any): any instance being voted
        instance (Model): vote instance
        user (User): user who is voting
        created (Boolean): True if the instance has been created or False otherwise.
    """

    if created and instance.vote != 'UNDONE':
        message_action = "up voted" if instance.vote == 'UPVOTE' else 'down voted'

        notification_obj = Notification.objects.create(
            user=post.user,
            message=f"{user.username} has {message_action} your {post_name}",
            origin='VOTE'
        )

        send_notification(f"notification_{post.user.id}", notification_obj)


def send_comment_notification(post_name, post, instance, user, created, **kwargs):
    """send comment notification to the post owner

    Args:
        post_name (str): the name of post being commented on. eg: question, gossip
        post (Any): any instance being voted but most likely a model instance
        instance (Comment): an instance of comment model
        user (User): user who is commenting
        created (Boolean): True if comment is created, False otherwise
    """

    if created:
        username = user.username

        # save user notification

        notification_obj = Notification.objects.create(
            user=post.user,
            message=f"{username} has commented on your {post_name}.",
            origin='COMMENT'
        )

        # send notification

        send_notification(f"notification_{post.user.id}", notification_obj)


def notify_interested_users(about='', **kwargs):
    """Notify all interesed users of a new post being created

    Args:
        about (str, optional): intresting instance name (just the correspoding label). Defaults to ''.
    """

    created = kwargs.get('created', False)
    instance = kwargs.get('instance', None)
    creator = kwargs.get('user', None)

    if created:
        tags = instance.tags.all()
        users = get_user_model().objects.filter(interested_topics__in=tags)
        users = set(users)
        channel_layer = get_channel_layer()

        # Send notification to user group
        for user in users:
            notification_obj = Notification.objects.create(
                user=user,
                origin='POST',
                message=f"{creator.username} has posted a {about} \"{instance.title}\""
            )

            # Send user notification
            send_notification(f"notification_{user.id}", notification_obj)
