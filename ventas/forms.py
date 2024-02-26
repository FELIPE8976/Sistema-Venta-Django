from django import forms
from django.core.exceptions import ValidationError
from .models import Product

class CreateNewProduct(forms.Form):
   name = forms.CharField(label='Enter the name of the new product', max_length=200)
   stock = forms.IntegerField(label='Enter the quantity')

   def clean_name(self):
      name = self.cleaned_data.get('name')
      if name:
         if Product.objects.filter(name =name).exists():
            raise ValidationError('This product already exist')
      return name
   
class DeleteProduct(forms.Form):
   product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Select a product to delete',empty_label='None')

class UpdateProduct(forms.Form):
   product = forms.ModelChoiceField(queryset=Product.objects.all(), label='Select a product to update')
   stock = forms.IntegerField(label='Enter a new quantity', min_value=0)
