from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from .models import Product, ProductCategory


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None):
    title = "Каталог товаров"
    # выводить будем только категории в которых есть товары
    product_category = ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    all_product = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()
    context = {
        'title': title,
        'all_product': all_product,
        'product_category': product_category,

    }
    return render(request, 'mainapp/products.html', context)
