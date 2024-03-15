from django.contrib import admin
from .models import Product,Carrito_products,Sell_history

admin.site.register(Product)
admin.site.register(Carrito_products)
admin.site.register(Sell_history)