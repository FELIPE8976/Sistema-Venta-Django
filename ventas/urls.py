from django.urls import path
from . import views

urlpatterns = [
   # path('', views.index, name='index'),
   path('new_product/', views.create_product, name='new_product'),
   path('update_product/', views.update_product, name='update_product'),
   path('delete_product/', views.delete_product, name='delete_product'),
   path('inventory/', views.inventory, name='inventory'),
   path('report/', views.report, name='report'),
   path('all_products/', views.all_products, name='all_products'),
   path('carrito/', views.carrito, name='carrito'),
   path('agregar_producto_carrito/', views.agregar_producto_carrito),
]