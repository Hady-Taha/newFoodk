from django import template
from customer.utils import customer_or_device
from store.models import Cart 
register = template.Library()


@register.simple_tag
def quantity(product, request):
    return Cart.objects.filter(customer=customer_or_device(request), product=product, order=False)[0].quantity
