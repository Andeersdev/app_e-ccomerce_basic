from django.db import models
from core.subcategory.models import Subcategory


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product/', null=False, blank=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'

    def __str__(self) -> str:
        return self.name
