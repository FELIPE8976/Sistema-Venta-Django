from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class CreateNewProduct(forms.Form):
   name = forms.CharField(label='Ingrese el nombre del producto', max_length=200)
   stock = forms.IntegerField(label='Ingrese la cantidad')

   def clean_name(self):
      name = self.cleaned_data.get('name')
      if name:
         if Product.objects.filter(name =name).exists():
            raise ValidationError('Este producto ya existe')
      return name
   
class DeleteProduct(forms.Form):
   product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Seleccione el producto a eliminar')

class UpdateProduct(forms.Form):
   product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Seleccione el producto a actualizar')
   stock = forms.IntegerField(label='Ingrese la nueva cantidad', min_value=0)
