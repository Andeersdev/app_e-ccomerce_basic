from django.db import models
from core.category.models import Category


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subcategory'

    def __str__(self) -> str:
        return self.name
