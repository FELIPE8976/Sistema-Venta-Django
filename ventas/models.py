from django.db import models

class Product(models.Model):
   name = models.CharField(max_length=200)
   stock = models.IntegerField(default=0)

   def __str__(self) -> str:
      return self.name