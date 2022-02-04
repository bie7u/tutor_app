from django import template
from reg_log.models import Client

register = template.Library()

@register.filter(name='phone_access')
def phone_access(request):
    a = Client.objects.filter(user=request.user, phone=None)
    return a 

    