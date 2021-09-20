from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from .models import Product, ProductCategory


def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    title = "Каталог товаров"
    all_product = Product.objects.all()
    # выводить будем только категории в которых есть товары
    product_category = ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    context = {
        'title': title,
        'all_product': all_product,
        'product_category': product_category
    }
    return render(request, 'mainapp/products.html', context)
