from django import template

from apps.notification.models import Notif

register = template.Library()


@register.simple_tag
def get_notifications(request):
    notif_read = Notif.objects.filter(user=request.user, read=True)
    notif_unread = Notif.objects.filter(user=request.user, read=False)
    has_notif = True if notif_unread.count() > 0 else False

    return {
        'read': notif_read,
        'unread': notif_unread,
        'has_notif': has_notif
    }
