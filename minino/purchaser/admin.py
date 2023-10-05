from django.contrib import admin
from .models import PurchaserModel
from catalog.models import CartModel

class CartModelInline(admin.TabularInline):
    model = CartModel
    extra = 0  # Para evitar mostrar formularios en blanco

@admin.register(PurchaserModel)
class PurchaserModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    inlines = [CartModelInline]
