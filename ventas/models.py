from functools import total_ordering
from django.db import models
from django.contrib.auth.models import User
import json

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
   
class Sell_history(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField()
    sell_date = models.DateTimeField(auto_now_add=True)
    product_list = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} - {self.total} - {self.sell_date}"

    def set_product_list(self, product_list):
        self.product_list = json.dumps(product_list)

    def get_product_list(self):
        return json.loads(self.product_list) if self.product_list else []