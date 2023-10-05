from django.db import models

# Create your models here.
class PurchaserModel(models.Model):
    name = models.CharField(max_length=50)
    phone = models.PositiveIntegerField()

