from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('new_product/', views.create_product, name='new_product'),
   path('update_product/', views.update_product, name='update_product'),
   path('delete_product/', views.delete_product, name='delete_product'),
   path('inventory/', views.inventory, name='inventory'),
]