from django.urls import path
from . import views

urlpatterns = [
   # path('', views.index, name='index'),
   path('inventory/new_product/', views.create_product, name='new_product'),
   path('inventory/update_product/', views.update_product, name='update_product'),
   path('inventory/delete_product/', views.delete_product, name='delete_product'),
   path('inventory/', views.inventory, name='inventory'),
   path('inventory/report/', views.report, name='report'),
   path('all_products/', views.all_products, name='all_products'),
   path('carrito/', views.carrito, name='carrito'),
   path('agregar_producto_carrito/', views.agregar_producto_carrito),
   path('delete_cart_product/', views.delete_cart_product),
   path('apply_discount/', views.apply_discount),
   path('discount/',views.discounts, name='discount'),
   path('sedes/', views.sedes, name='sedes'),
   path('bill/', views.bill, name='bill'),
   path('history/', views.buy, name='history')
]