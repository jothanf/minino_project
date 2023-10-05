from django.urls import path
from . import views

urlpatterns = [
    path('<int:purchaser_id>', views.catalog_home, name='catalog_home'),
    path('select_products/<int:category_id>', views.select_products, name='select_products'),
    path('select_category/<int:store_id>/', views.select_category, name='select_category'),
    path('select_store/', views.select_store, name='select_store'),
    path('view_cart/<int:cart_id>', views.view_cart, name='view_cart'),
    path('prosses_order/', views.prosses_order, name='prosses_order'),
    path('finish_purchase/', views.finish_purchase, name='finish_purchase'),
    path('admin_stores/', views.admin_stores, name='admin_stores'),
    path('create_store/', views.create_store, name='create_store'),
    path('create_category/', views.create_category, name='create_category'),
    path('create_provider/', views.create_provider, name='create_provider'),
    path('create_product/', views.create_product, name='create_product'),
]