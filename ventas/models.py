from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
   name = models.CharField(max_length=200)
   stock = models.IntegerField(default=0)
   unit_price = models.IntegerField(default = 0)
   discount = models.IntegerField(default=0)
   have_discount = models.BooleanField(default=False)


   def __str__(self):
      return self.name


class Carrito_products(models.Model):
   name = models.ForeignKey(Product, on_delete=models.CASCADE)
   units = models.IntegerField(default=0)
   have_coupon = models.BooleanField(default=0)
   unit_price = models.IntegerField(default = 0)
   total = models.IntegerField(default=0)
   user = models.ForeignKey(User, on_delete=models.CASCADE)

   def __str__(self):
      return self.name.name + ' by ' + self.user.username