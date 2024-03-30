from django import template
from tixx.models import Figure

register = template.Library()

@register.filter(name='getFigure')
def get_figure(figure_id):
    return Figure.objects.get(id=figure_id)