"""
Definition of models.
"""

from django.db import models

# Create your models here.


class Items(models.Model):
    item_name = models.CharField(max_length=30)
    item_price = models.IntegerField(default='0')
