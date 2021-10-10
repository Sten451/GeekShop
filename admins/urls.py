from django.urls import path

from .views import index, UserCreateView, UserUpdateView, UserListView, UserDeleteView, CategoryListView, \
    CategoryUpdateView, CategoryCreateView, CategoryDeleteView, ProductListView, ProductDeleteView, ProductCreateView, ProductUpdateView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),

    path('users/', UserListView.as_view(), name='admins_user'),
    path('users-create/', UserCreateView.as_view(), name='admins_user_create'),
    path('users-update/<int:pk>/', UserUpdateView.as_view(), name='admins_user_update'),
    path('users-delete/<int:pk>/', UserDeleteView.as_view(), name='admins_user_delete'),

    path('categories/', CategoryListView.as_view(), name='admins_category'),
    path('categories-update/<int:pk>/', CategoryUpdateView.as_view(), name='admins_category_update'),
    path('categories-create/', CategoryCreateView.as_view(), name='admins_category_create'),
    path('categories-delete/<int:pk>/', CategoryDeleteView.as_view(), name='admins_category_delete'),

    path('products/', ProductListView.as_view(), name='admins_products'),
    path('products-update/<int:pk>/', ProductUpdateView.as_view(), name='admins_products_update'),
    path('products-create/', ProductCreateView.as_view(), name='admins_products_create'),
    path('products-delete/<int:pk>/', ProductDeleteView.as_view(), name='admins_products_delete'),]
