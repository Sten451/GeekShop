from django.shortcuts import render

# Create your views here.
from django.db.models import Count
from .models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None, page_id=1):
    title = "Каталог товаров"
    # выводить будем только категории в которых есть товары
    product_category = ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    products = Product.objects.filter(category_id=category_id) if category_id != None else Product.objects.all()

    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page_id)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(Paginator.num_pages)

    context = {
        'title': 'Каталог',
        'product_category': product_category,
    }
    context.update({'products': products_paginator})
    return render(request, 'mainapp/products.html', context)
