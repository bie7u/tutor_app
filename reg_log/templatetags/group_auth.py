from django import template

# Checks which group now is use.

register = template.Library()

@register.filter(name='group_auth')
def group_auth(request):
    group = None
    if str(request.user.groups.get()) == 'tutor':
        group = 1
    if str(request.user.groups.get()) == 'customer':
        group = 2
    if str(request.user.groups.get()) == 'admin':
        group = 3
    return group