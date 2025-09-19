import flet as ft
import time
from datetime import datetime
from ..controllers.controllers import FacturaController

def add_to_cart(app, e):
    if not hasattr(app, 'selected_producto_venta'):
        return
    try:
        cantidad = int(app.cantidad.value)
        if cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        if cantidad > app.selected_producto_venta.stock:
            raise ValueError(f"Stock insuficiente. Solo quedan {app.selected_producto_venta.stock} unidades")
        app.carrito.append({
            'producto': app.selected_producto_venta,
            'cantidad': cantidad,
            'precio': app.selected_producto_venta.precio,
            'subtotal': cantidad * app.selected_producto_venta.precio
        })
        
        # RESETEA EL PRODUCTO SELECCIONADO DESPUÉS DE AGREGAR AL CARRITO
        app.selected_producto_venta = None
        if hasattr(app, 'producto_seleccionado_text'):
            app.producto_seleccionado_text.value = "Producto seleccionado: "
        if hasattr(app, 'cantidad'):
            app.cantidad.disabled = True
            app.cantidad.value = "1"
            
        update_carrito(app)
        
    except Exception as ex:
        app.page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(str(ex)), actions=[ft.TextButton("Cerrar", on_click=lambda e: app.page.dialog.close())])
        app.page.dialog.open = True
        app.page.update()
        app.page.add(app.page.dialog)
        # Agregar el diálogo a la página para que se muestre correctamente
        app.page.add(app.page.dialog)

def handle_cart_click(app, index):
    """Manejar clics en el carrito - simple clic o doble clic"""
    current_time = time.time()
    
    # Verificar si es un doble clic (dentro de 0.5 segundos)
    if app.last_click_time and (current_time - app.last_click_time) < 0.5:
        # Doble clic - entrar en modo edición
        app.cart_edit_mode = True
        app.selected_cart_index = index
        update_carrito(app)
    else:
        # Clic simple - seleccionar item
        select_cart_item(app, index)
    
    app.last_click_time = current_time

def select_cart_item(app, index):
    """Seleccionar un item del carrito para edición/eliminación"""
    if app.selected_cart_index == index:
        # Si ya está seleccionado, deseleccionar
        app.selected_cart_index = None
        app.cart_buttons_visible = False
    else:
        # Seleccionar nuevo item
        app.selected_cart_index = index
        app.cart_buttons_visible = True

    # Mostrar/ocultar botones de edición/eliminación
    if hasattr(app, 'editar_carrito_button') and hasattr(app, 'eliminar_carrito_button'):
        app.editar_carrito_button.visible = app.cart_buttons_visible
        app.eliminar_carrito_button.visible = app.cart_buttons_visible

    # Actualizar display del carrito
    update_carrito(app)
    app.page.update()

def editar_item_carrito(app, e):
    """Entrar en modo edición para el item seleccionado"""
    if app.selected_cart_index is not None:
        app.cart_edit_mode = True
        update_carrito(app)
        app.page.update()

def eliminar_item_carrito(app, e):
    """Eliminar el item seleccionado del carrito"""
    if app.selected_cart_index is not None:
        # Eliminar el item del carrito
        del app.carrito[app.selected_cart_index]
        
        # Resetear selección
        app.selected_cart_index = None
        app.cart_buttons_visible = False
        app.cart_edit_mode = False
        
        # Ocultar botones
        if hasattr(app, 'editar_carrito_button') and hasattr(app, 'eliminar_carrito_button'):
            app.editar_carrito_button.visible = False
            app.eliminar_carrito_button.visible = False
        
        # Actualizar carrito
        update_carrito(app)
        app.page.update()

def update_cart_quantity(app, index, new_quantity):
    """Actualizar la cantidad de un item en el carrito"""
    try:
        new_qty = int(new_quantity)
        if new_qty > 0:
            app.carrito[index]['cantidad'] = new_qty
            app.carrito[index]['subtotal'] = new_qty * app.carrito[index]['precio']
    except ValueError:
        # Si no es un número válido, no hacer nada
        pass

def confirm_cart_edit(app, index):
    """Confirmar la edición y salir del modo edición"""
    app.cart_edit_mode = False
    update_carrito(app)
    app.page.update()

def update_carrito(app):
    app.carrito_list.rows.clear()
    total = 0
    for i, item in enumerate(app.carrito):
        precio_ves = item['precio'] * app.exchange_rate
        subtotal_ves = item['subtotal'] * app.exchange_rate

        # Determinar si esta fila está seleccionada
        is_selected = (app.selected_cart_index == i)
        row_color = ft.Colors.BLUE_50 if is_selected and not app.dark_mode else (ft.Colors.BLUE_900 if is_selected and app.dark_mode else None)

        # Crear celdas con funcionalidad de edición si está en modo edición
        if app.cart_edit_mode and is_selected:
            # Modo edición: mostrar TextField para cantidad
            cantidad_cell = ft.DataCell(
                ft.Container(
                    content=ft.TextField(
                        value=str(item['cantidad']),
                        width=80,
                        height=35,
                        text_align=ft.TextAlign.CENTER,
                        border_radius=5,
                        on_change=lambda e, idx=i: update_cart_quantity(app, idx, e.control.value),
                        on_submit=lambda e, idx=i: confirm_cart_edit(app, idx)
                    ),
                    alignment=ft.alignment.center
                )
            )
        else:
            # Modo normal: mostrar texto
            cantidad_cell = ft.DataCell(ft.Text(str(item['cantidad'])))

        app.carrito_list.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item['producto'].nombre)),
                    cantidad_cell,
                    ft.DataCell(ft.Text(f"{item['precio']:.2f}")),
                    ft.DataCell(ft.Text(f"{precio_ves:.2f}")),
                    ft.DataCell(ft.Text(f"{item['subtotal']:.2f}")),
                ],
                on_select_changed=lambda e, idx=i: handle_cart_click(app, idx),
                color=row_color
            )
        )
        total += item['subtotal']
    total_ves = total * app.exchange_rate
    app.total_label.content.value = f"Total: ${total:.2f} / Bs.{total_ves:.2f}"
    app.page.update()

def finalizar_venta(app, e):
    if not app.carrito:
        return

    try:
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = sum(item['subtotal'] for item in app.carrito)
        detalles = []

        # Primero verificar que haya suficiente stock para todos los productos
        for item in app.carrito:
            producto = item['producto']  # Este es el objeto Producto
            cantidad = item['cantidad']

            if cantidad > producto.stock:
                raise ValueError(f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}, Cantidad solicitada: {cantidad}")

        # Si todo está bien, procesar la venta
        for item in app.carrito:
            producto = item['producto']  # Este es el objeto Producto
            cantidad = item['cantidad']
            precio = item['precio']

            # Actualizar el stock del producto
            app.producto_controller.update_producto_stock(producto.id, producto.stock - cantidad)

            # Agregar al detalle de la venta
            detalles.append({
                'producto_id': producto.id,
                'cantidad': cantidad,
                'precio': precio
            })

        # Registrar la venta
        venta_id = app.venta_controller.registrar_venta(fecha, total, detalles)

        # Crear factura automáticamente
        factura_controller = FacturaController()
        # Sin datos de cliente
        factura_id = factura_controller.crear_factura(fecha, total, detalles)

        # Limpiar el carrito
        app.carrito.clear()
        update_carrito(app)

        # Preguntar si quiere imprimir la factura
        def imprimir_factura(e):
            app.page.dialog.open = False
            # Generar PDF
            from .factura_view import generar_pdf_factura
            factura = factura_controller.get_by_id(factura_id)
            if factura:
                archivo_pdf = generar_pdf_factura(factura)
                app.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Factura exportada a PDF: {archivo_pdf}"),
                    bgcolor=ft.Colors.GREEN_600
                )
                app.page.snack_bar.open = True
            app.page.update()

        def cerrar_dialogo(e):
            app.page.dialog.open = False
            app.page.update()

        # Mostrar diálogo preguntando si imprimir
        app.page.dialog = ft.AlertDialog(
            title=ft.Text("✅ Venta Finalizada"),
            content=ft.Text(f"Total: ${total:.2f}\nFactura #{factura_id} creada exitosamente.\n\n¿Desea imprimir la factura?"),
            actions=[
                ft.TextButton("No", on_click=cerrar_dialogo),
                ft.ElevatedButton("Sí, Imprimir", on_click=imprimir_factura, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE))
            ]
        )
        app.page.dialog.open = True

        # Recargar productos para reflejar los nuevos stocks
        app.load_productos()

    except Exception as ex:
        app.page.dialog = ft.AlertDialog(
            title=ft.Text("❌ Error"),
            content=ft.Text(str(ex)),
            actions=[ft.TextButton("Cerrar", on_click=lambda e: app.page.dialog.close())]
        )
        app.page.dialog.open = True

    app.page.update()

def open_product_catalog_modal(app, e):
    """Abrir modal del catálogo de productos"""
    # Crear lista de productos disponibles (con stock > 0)
    available_products = [p for p in app.productos if p.stock > 0]

    if not available_products:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text("No hay productos disponibles en stock"),
            bgcolor=ft.Colors.ORANGE_600
        )
        app.page.snack_bar.open = True
        app.page.update()
        return

    def cerrar_dialogo(e):
        app.page.dialog.open = False
        app.page.update()

    def seleccionar_producto(producto):
        """Función para seleccionar un producto y cerrar modal"""
        app.selected_producto_venta = producto
        # Actualizar texto seleccionado en la vista de ventas
        if hasattr(app, 'producto_seleccionado_text'):
            app.producto_seleccionado_text.value = f"Producto seleccionado: {producto.nombre}"
        # Habilitar campo cantidad
        if hasattr(app, 'cantidad'):
            app.cantidad.disabled = False
            app.cantidad.value = "1"
        # Cerrar modal
        app.page.dialog.open = False
        app.page.update()

    product_rows = []
    for producto in available_products:
        product_rows.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(producto.nombre, size=16, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Precio: ${producto.precio:.2f} | Stock: {producto.stock}", size=12, color=ft.Colors.BLUE_GREY_600),
                            ],
                            spacing=5,
                            expand=True
                        ),
                        ft.ElevatedButton(
                            "Seleccionar",
                            on_click=lambda e, p=producto: seleccionar_producto(p),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.BLUE_600,
                                color=ft.Colors.WHITE
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=ft.padding.symmetric(vertical=10, horizontal=15),
                border=ft.border.all(1, ft.Colors.BLUE_GREY_200),
                border_radius=10,
                margin=ft.margin.symmetric(vertical=5)
            )
        )

    # Crear modal siguiendo el patrón de factura_view
    app.page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Catálogo de Productos", size=20, weight=ft.FontWeight.BOLD),
        content=ft.Container(
            content=ft.Column(
                controls=product_rows,
                scroll=ft.ScrollMode.AUTO,
                height=400,
                spacing=5
            ),
            height=400,
            width=600
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=cerrar_dialogo)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    app.page.dialog.open = True
    app.page.update()
    # Agregar el diálogo a la página para que se muestre correctamente
    app.page.add(app.page.dialog)

def select_product_for_sale(app, e, idx):
    """Handle product selection for sale"""
    app.selected_producto_venta = app.productos[idx]

    # Update the selected product display in the ventas view
    if hasattr(app, 'producto_seleccionado_text'):
        app.producto_seleccionado_text.value = f"Producto seleccionado: {app.selected_producto_venta.nombre}"

    # Enable quantity field since we have a selected product
    if hasattr(app, 'cantidad'):
        app.cantidad.disabled = False
        app.cantidad.value = "1"  # Reset to default quantity

    # Automatically return to ventas view
    app.change_view("ventas")

def build_ventas_view(app):
    # Initialize form fields
    app.cantidad = ft.TextField(
        label="Cantidad",
        value="1",
        width=150,
        border_radius=10,
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_800
    )
    app.cantidad.disabled = app.selected_producto_venta is None

    app.seleccionar_button = ft.ElevatedButton(
        "Seleccionar",
        on_click=lambda e: open_product_catalog_modal(app, e),
        icon=ft.Icons.LIST,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )
    )

    app.aceptar_button = ft.ElevatedButton(
        "Aceptar",
        on_click=lambda e: add_to_cart(app, e),
        icon=ft.Icons.CHECK,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )
    )

    # Botones para editar/eliminar productos del carrito
    app.editar_carrito_button = ft.ElevatedButton(
        "Editar",
        on_click=lambda e: editar_item_carrito(app, e),
        icon=ft.Icons.EDIT,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.ORANGE_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
        visible=False
    )

    app.eliminar_carrito_button = ft.ElevatedButton(
        "Eliminar",
        on_click=lambda e: eliminar_item_carrito(app, e),
        icon=ft.Icons.DELETE,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        ),
        visible=False
    )

    # Enhanced cart display
    app.carrito_list = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio USD", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio VES", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        width=900,
        height=300,  # Aumentado para mejor visualización
        border_radius=10,
        heading_row_height=50,
        data_row_min_height=45,
        data_row_max_height=60,
    )

    app.total_label = ft.Container(
        content=ft.Text("Total: $0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.GREEN_50 if not app.dark_mode else ft.Colors.GREEN_900,
        border_radius=15
    )

    app.finalizar_venta_button = ft.ElevatedButton(
        "Finalizar Venta",
        on_click=lambda e: finalizar_venta(app, e),
        icon=ft.Icons.PAYMENT,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=30, vertical=15)
        )
    )

    # Container for selected product display
    producto_seleccionado_nombre = app.selected_producto_venta.nombre if app.selected_producto_venta else ""
    app.producto_seleccionado_text = ft.Text(f"Producto seleccionado: {producto_seleccionado_nombre}", size=14)
    app.productos_container = ft.Container(content=None, expand=True)  # Will hold the product list when opened

    # Poblar el carrito con los datos actuales
    update_carrito(app)

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Text("Ventas", size=24, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(bottom=10)
            ),

            # Product Selection Section
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=app.producto_seleccionado_text,
                                        padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                        bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                                        border_radius=10,
                                        expand=True
                                    ),
                                    app.cantidad,
                                    app.seleccionar_button,
                                    app.aceptar_button
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=ft.padding.symmetric(vertical=5)
                        ),
                    ],
                    spacing=10
                ),
                padding=15,
                bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
                )
            ),

            # Cart Section
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    app.carrito_list,
                                    ft.Divider(height=15),
                                    # Botones de edición/eliminación (ocultos inicialmente)
                                    ft.Row(
                                        controls=[
                                            app.editar_carrito_button,
                                            app.eliminar_carrito_button,
                                            ft.Container(expand=True),  # Espaciador
                                            app.total_label,
                                            app.finalizar_venta_button
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                                    )
                                ],
                                spacing=15
                            ),
                            padding=15,
                            bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=8,
                                color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
                            )
                        )
                    ],
                    spacing=15
                ),
                padding=ft.padding.symmetric(vertical=5)
            )
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO
    )
