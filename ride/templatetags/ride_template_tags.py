from django import template
from ride.models import ServicePage

register = template.Library()

@register.inclusion_tag('ride/categories.html')
def get_category_list(current_category=None):
    return {'services': ServicePage.objects.all(), 'current_service': current_service}
