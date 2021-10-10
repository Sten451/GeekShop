from django import template
from mainapp.models import Product

register = template.Library()

@register.inclusion_tag('mainapp/tags/last_product.html')
def get_last_product():
    product_last = Product.objects.order_by('created_at')[:3]
    return {'last_product': product_last}


