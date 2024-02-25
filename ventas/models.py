from django.db import models

class Product(models.Model):
   name = models.CharField(max_length=200)
   stock = models.IntegerField(default=0)

   def __str__(self):
      return self.name


class Carrito_products(models.Model):
   name = models.ForeignKey(Product, on_delete=models.CASCADE)
   units = models.IntegerField(default=0)

   def __str__(self):
      return self.name.name