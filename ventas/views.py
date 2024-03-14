from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Product, Carrito_products
from .forms import CreateNewProduct, UpdateProduct, DeleteProduct
from io import BytesIO
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta, time


def create_product(request):
   if request.method == 'POST':
      form = CreateNewProduct(request.POST)
      if form.is_valid():
         name = form.cleaned_data['name']
         stock = form.cleaned_data['stock']
         price = form.cleaned_data['price']
         Product.objects.create(name=name, stock=stock, unit_price=price)
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
   queryset = request.GET.get("search")
   products = Product.objects.all()
   if queryset:
      products = Product.objects.filter(name__icontains=queryset)
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
   carrito_products = Carrito_products.objects.filter(user=request.user)
   return render(request, 'comprar/carrito.html', {'carrito_products': carrito_products})

def notify_low_stock(product, stock):
   subject = 'Se agota un producto'
   message = 'Quedan pocas unidades del producto:'
   template = render_to_string('inventory/email.html', {
      'message': message,
      'product': product,
      'units': stock,
   })

   email = EmailMessage(
      subject,
      template,
      settings.EMAIL_HOST_USER,
      ['carloscamacho0602@gmail.com']
   )

   email.fail_silently = False
   email.send()


def agregar_producto_carrito(request):
   if request.method == 'POST':
      product_id = request.POST.get('product_id')
      quantity = int(request.POST.get('quantity'))
      product = Product.objects.get(pk=product_id)
      user = request.user
      if 1 <= quantity <= product.stock:
         total = quantity * product.unit_price
         Carrito_products.objects.create(name=product, units=quantity, total=total, user=user)
         product.stock -= quantity
         product.save()
         if product.stock <= 5:
            notify_low_stock(product, product.stock)
      return redirect('all_products')
   return render(request, 'comprar/all_products.html')

def sedes(request):
   sedes = [
        {'nombre': 'North', 'direccion' : 'Cl. 38 Nte. #6N – 45, Cali, Valle del Cauca', 'hora_apertura': time(6, 0), 'hora_cierre': time(16, 0), 'link' : 'https://www.google.com/maps/dir//Centro+Comercial+Chipichape,+Cl.+38+Nte.+%236N+–+45,+Cali,+Valle+del+Cauca/@3.4742296,-76.5320935,17z/data=!4m12!1m2!2m1!1schipichape+maps!4m8!1m0!1m5!1m1!1s0x8e30a618c17d3bf7:0x516c5b91fa92e1b9!2m2!1d-76.5278784!2d3.4760132!3e2?entry=ttu'},
        {'nombre': 'South', 'direccion' : 'Cra. 100 #5-169, Cali, Valle del Cauca', 'hora_apertura': time(9, 0), 'hora_cierre': time(18, 0), 'link' : 'https://www.google.com/maps/dir//Unicentro+Cali,+Carrera+100,+Las+Vegas,+Cali,+Valle+del+Cauca/@3.374148,-76.5803696,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x8e30a17ab8179221:0xcfd9c65aada830d9!2m2!1d-76.5391697!2d3.3740632!3e2?entry=ttu'},
    ]
   hora_actual_colombia = datetime.utcnow() - timedelta(hours=5)
   hora_actual_colombia = hora_actual_colombia.time()
   for sede in sedes:
        if sede['hora_apertura'] <= hora_actual_colombia <= sede['hora_cierre']:
            sede['estado'] = "Open"
        else:
            sede['estado'] = "Close"
   return render(request, 'comprar/sedes.html', {'sedes': sedes})

def delete_cart_product(request):
   if request.method == 'POST':
      cart_product_id = request.POST.get('cart_product_id')
      cart_product = Carrito_products.objects.get(id=cart_product_id)
      product = Product.objects.get(id=cart_product.name_id)
      product.stock += cart_product.units
      product.save()
      cart_product.delete()
      return redirect('carrito')
   return render(request, 'comprar/carrito.html')

def apply_discount(request):
   if request.method == 'POST':
      discount_id = request.POST.get('discount_id')
      discount_value = request.POST.get('discount_value')
      cart_product = Carrito_products.objects.get(id=discount_id)
      product = Product.objects.get(id=cart_product.name_id)
      new_price = cart_product.units * (product.unit_price - (product.unit_price * (int(discount_value) / 100)))
      cart_product.total = new_price
      cart_product.have_coupon = 1
      cart_product.save()
      return redirect('carrito')
   return render(request, 'comprar/carrito.html')
def discounts(request):
   products = Product.objects.all()
   return render(request, 'comprar/discounts.html',{
      'products': products
   })

def delete_cart_product(request):
   if request.method == 'POST':
      cart_product_id = request.POST.get('cart_product_id')
      cart_product = Carrito_products.objects.get(id=cart_product_id)
      product = Product.objects.get(id=cart_product.name_id)
      product.stock += cart_product.units
      product.save()
      cart_product.delete()
      return redirect('carrito')
   return render(request, 'comprar/carrito.html')

def apply_discount(request):
   if request.method == 'POST':
      discount_id = request.POST.get('discount_id')
      discount_value = request.POST.get('discount_value')
      cart_product = Carrito_products.objects.get(id=discount_id)
      product = Product.objects.get(id=cart_product.name_id)
      new_price = cart_product.units * (product.unit_price - (product.unit_price * (int(discount_value) / 100)))
      cart_product.total = new_price
      cart_product.have_coupon = 1
      cart_product.save()
      return redirect('carrito')
   return render(request, 'comprar/carrito.html')

