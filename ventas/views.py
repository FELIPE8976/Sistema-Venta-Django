from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Carrito_products
from .forms import CreateNewProduct, UpdateProduct, DeleteProduct
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# def index(request):
#    return render(request, 'index.html')

def create_product(request):
   if request.method == 'POST':
      form = CreateNewProduct(request.POST)
      if form.is_valid():
         name = form.cleaned_data['name']
         stock = form.cleaned_data['stock']
         Product.objects.create(name=name, stock=stock)
         return redirect('new_product')
   else:
      form = CreateNewProduct()
   return render(request, 'inventory/create_product.html', {'form': form})

def update_product(request):
   if request.method == 'POST':
      form = UpdateProduct(request.POST)
      if form.is_valid():
         product = form.cleaned_data['product']
         stock = form.cleaned_data['stock']
         product.stock = stock
         product.save()
         return redirect('update_product')
   else:
      form = UpdateProduct()
   return render(request, 'inventory/update_product.html', {'form': form})

def delete_product(request):
   if request.method == 'POST':
      form = DeleteProduct(request.POST)
      if form.is_valid():
         product = form.cleaned_data['product']
         product.delete()
         return redirect('delete_product')
   else:
      form = DeleteProduct()
   return render(request, 'inventory/delete_product.html', {'form': form})

def inventory(request):
   products = Product.objects.all()
   return render(request, 'inventory/show_products.html', {'products': products})

def report(request):
   date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
   products = Product.objects.all().order_by('stock')
   buffer = BytesIO()
   pdf = SimpleDocTemplate(buffer, pagesize=letter) 
   data = [['Name','Stock']]

   for product in products:
      data.append([product.name, str(product.stock)])

   tabla = Table(data)

   style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F37A00')),
                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                     ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FCC691')),
                     ('GRID', (0, 0), (-1, -1), 1, colors.black)])

   # Elementos del pdf
   tabla.setStyle(style)
   styles = getSampleStyleSheet()
   fecha = Paragraph(f"Date: {date}\n")
   titulo = Paragraph("Inventory report", styles['Title'])
   titulo.spaceAfter = 30
   texto = Paragraph("All available products:", styles['Normal'])
   texto.spaceAfter = 20 

   # Crear PDF
   pdf.build([fecha,titulo,texto,tabla])

   # Devolver el PDF como una respuesta HTTP
   response = HttpResponse(content_type='application/pdf')
   response['Content-Disposition'] = 'attachment; filename="Reporte_inventario.pdf"'
   response.write(buffer.getvalue())
   buffer.close()
   return response

def all_products(request):
   products = Product.objects.all()
   return render(request, 'comprar/all_products.html', {'products': products})

def carrito(request):
   carrito_products = Carrito_products.objects.all()
   return render(request, 'comprar/carrito.html', {'carrito_products': carrito_products})

def agregar_producto_carrito(request):
   if request.method == 'POST':
      product_id = request.POST.get('product_id')
      quantity = int(request.POST.get('quantity'))
      product = Product.objects.get(pk=product_id)
      if 1 <= quantity <= product.stock:
         Carrito_products.objects.create(name=product, units=quantity)
         product.stock -= quantity
         product.save()
      return redirect('all_products')
   return render(request, 'comprar/all_products.html')
