from django import template
from reg_log.models import Client

# Return all Client data (users)

register = template.Library()

@register.filter(name='all_data')
def all_data(request):
    form = [i for i in Client.objects.filter(user=request.user)]
    form_two = [i for i in form]
    return form_two