from django import template
from ride.models import ServicePage

register = template.Library()

@register.inclusion_tag('ride/services.html')
def get_service_list(current_service=None):
    return {'services': ServicePage.objects.all(), 'current_service': current_service}
