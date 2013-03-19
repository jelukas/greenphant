from django import template
from django.contrib.auth.models import User
from ..models import Message

register = template.Library()

@register.filter(name='user_count_messages')
def user_count_messages(user_id):
    return Message.objects.filter(to_user_id=user_id, is_read=False).order_by('-created_at').count()
