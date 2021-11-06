from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import ListView, DetailView
from .models import Product, ProductCategory
from django.conf import settings
from django.core.cache import cache

def index(request):
    return render(request, 'mainapp/index.html')

class AllProductCategory:
    model = ProductCategory

    #def get_active_category(self):
    #    return ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)

    def get_active_category(self):
        if settings.LOW_CACHE:
            key = 'links_category21'
            link_category21 = cache.get(key)
            if link_category21 is None:
                link_category21 = ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
                cache.set(key, link_category21)
            return link_category21
        else:
            return ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)


class ProductsView(AllProductCategory, ListView):
    model = Product
    title = 'Каталог продуктов'
    template_name = 'mainapp/products.html'
    context_object_name = 'ListProducts'
    paginate_by = 3

    """def get_queryset(self):
        category = self.kwargs.get('category_id', None)
        if category is not None:
            return Product.objects.filter(category=category).select_related('category')
        return Product.objects.all().select_related('category')"""
    # наверное это не работает, хотя хз
    def get_queryset(self):
        category = self.kwargs.get('category_id', None)
        if settings.LOW_CACHE:
            key = 'links_category'
            link_category = cache.get(key)
            if link_category is None:
                link_category = self.verify_category(category)
                cache.set(key, link_category)
            return link_category
        else:
            return self.verify_category(category)


    def verify_category(self,category):
        if category is not None:
            link_category2 = Product.objects.filter(category=category).select_related('category')
        else:
            link_category2 = Product.objects.all().select_related('category')
        return link_category2

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = self.get_product(self.kwargs.get('pk'))
        context['categories'] = ProductCategory.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
        return context


    def get_product(self, pk):
        if settings.LOW_CACHE:
            key = f'product{pk}'
            product = cache.get(key)
            if product is None:
                product = get_object_or_404(Product,pk=pk)
                cache.set(key, product)
            return product
        else:
            return get_object_or_404(Product,pk=pk)