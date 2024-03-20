
from django import template

register = template.Library()

# Converts the users rating out of 5 stars into a list,
# then indicates if it s a full (1), half (0.5), or (0) star.
# i.e  3.5 STAR Rating = [1, 1, 1, 0.5, 0]

@register.filter(name='starRange')
def starRange(value):
    fullStar = int(value)
    halfStar = value - fullStar >= 0.5
    emptyStar = 5 - fullStar - halfStar

    stars = [1] * fullStar
    if halfStar:
        stars.append(0.5)
    stars += [0] * emptyStar
    
    return stars