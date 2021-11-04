from django.shortcuts import render
from django.db.models import Count
from django.views.generic import ListView
from .models import Product, ProductCategory


def index(request):
    return render(request, 'mainapp/index.html')

class AllProductCategory:
    model = ProductCategory

    def get_active_category(self):
        return ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)


class ProductsView(AllProductCategory, ListView):
    model = Product
    title = 'Каталог продуктов'
    template_name = 'mainapp/products.html'
    context_object_name = 'ListProducts'
    paginate_by = 3

    def get_queryset(self):
        category = self.kwargs.get('category_id', None)
        if category is not None:
            return Product.objects.filter(category=category).select_related('category')
        return Product.objects.all().select_related('category')

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        return context
