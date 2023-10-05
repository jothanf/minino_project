from django import forms
from .models import StoreModel, CategoryModel, ProviderModel, ProductModel

class StoreForm(forms.ModelForm):
    class Meta:
        model = StoreModel
        fields = ['store_name', 'phone']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'store']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = ProviderModel
        fields = ['provider_name', 'phone', 'address']

class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['product_name', 'categories', 'price_purchase', 'price_sale', 'providers']
