from django.contrib import admin
from .models import StoreModel, ProviderModel, CategoryModel, ProductModel, CartModel

@admin.register(StoreModel)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'phone')

@admin.register(ProviderModel)
class ProviderModelAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'phone', 'address')

@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price_purchase', 'price_sale')
    filter_horizontal = ('categories', 'providers')  # This allows selecting categories and providers easily.

