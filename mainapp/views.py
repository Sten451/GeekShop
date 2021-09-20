from django.shortcuts import render

# Create your views here.
from .models import Product, ProductCategory


def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    title = "Каталог товаров"
    all_product = Product.objects.all()
    product_category = ProductCategory.objects.all()
    context = {
        'title': title,
        'all_product': all_product,
        'product_category': product_category
    }
    return render(request, 'mainapp/products.html', context)
