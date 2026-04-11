from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:id>/', views.product_update, name='product_update'),
    path('delete/<int:id>/', views.product_delete, name='product_delete'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]