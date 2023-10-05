from django.db import models
from purchaser.models import PurchaserModel
from datetime import datetime

class StoreModel(models.Model):
    store_name = models.CharField(max_length=50)
    phone = models.PositiveIntegerField()

    def __str__(self):
        return self.store_name

class ProviderModel(models.Model):
    provider_name = models.CharField(max_length=50)
    phone = models.PositiveIntegerField()
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.provider_name

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=50)
    store = models.ForeignKey(StoreModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.category_name

class ProductModel(models.Model):
    product_name = models.CharField(max_length=50)
    categories = models.ManyToManyField(CategoryModel)
    price_purchase = models.PositiveIntegerField()
    price_sale = models.PositiveIntegerField()
    providers = models.ManyToManyField(ProviderModel)
    product_img = models.ImageField(upload_to='products_img0/', null=True, blank=True)

    def __str__(self):
        return self.product_name

class CartModel(models.Model):
    STATE_CHOICES = (
        ('in_process', 'In Process'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )

    purchaser = models.ForeignKey(PurchaserModel, on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel)
    total_price = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    purchase_datetime = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Cart #{self.id}'
    
class ProductInCart(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    partial_price = models.PositiveIntegerField()
