from django import template
register = template.Library()

@register.filter(name='rank')
def rank(request):
    rank = None
    if len(request.user.groups.all()) > 0:
        rank = request.user.groups.all()[0].name
    return rank