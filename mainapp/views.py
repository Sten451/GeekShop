from django.shortcuts import render
import json
import os

# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    with open(os.path.join("mainapp/fixtures/db.json"), "r", encoding="utf-8") as read_file:
        data = json.load(read_file)
    return render(request, 'mainapp/products.html', data)


"""
def test(request):
    context = {
        'title': 'geekshop',
        'header': 'Welcome',
        'user': 'Sten',
        'products': [{'name': 'Худи черного цвета с монограммами adidas Originals', 'price':'6 090'},
                   {'name': 'Синяя куртка The North Face', 'price': '23 725'},
                   {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390'},
                   {'name': 'Черный рюкзак Nike Heritage', 'price': '2 340'},
                   ]

    }
    return render(request, 'mainapp/test.html', context)
"""