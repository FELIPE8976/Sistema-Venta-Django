# Sistema-Venta-Django

## Tecnologias usadas
* Django
* ReportLab
* SQLite2

### Descripción
El proyecto busca realizar un sistema POS, el cual distingue entre dos diferentes roles (Administrador - Vendedor). Esta plataforma se divide en las siguientes partes:

*Inventory:* Permite realizar el CRUD al inventario este solo puede ser visualizado por el administrador.

*Login:* Permite ingresar al vendedor o administrados a la plataforma.

*Discount:* Muestra los productos que cuentan con descuento en ese momento.

*Home:* Mensaje de bienvenida a la plataforma.

*History:* Muestra las ventas realizadas por el vendedor

*Cart:* Muestra las caracteristicas de la venta que esta realizando (Productos - Cantidad - Total - Calcular cambio). Este tambien permite crear una factura mediante "Bill" y agregar al historial mediante "Buy".
**Nota**: Se debe realizar primero la factura y luego añadir al historial.

*Available products:* Muestra los productos disponibles. Esta vista esta diseñada para que el vendedor pueda añadir al carrito los productos que desea el cliente.

*Stores:* Vista informativa. Se visualiza sin iniciar sesión y muestra de manera interactiva el estado de las diferentes sedes con las que cuenta el negocio/empresa.

# Nota
La creación de usuarios usa la tabla proveniente de Django, es decir que:

* *Vendedor:* Se crea mediante el uso de la ruta .../signup/. Esta ruta no esta destinada a ser mostrada en el producto final es unicamente para facilitar la creación del vendedor.
*  *Administrador:* Se crea haciendo uso del comando de la función que se encuentra en el manage.py de Django """ python manage.py createsuperuser """
