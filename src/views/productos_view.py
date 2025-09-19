import flet as ft
from ..utils.exchange_rate import ExchangeRateService

def load_productos(app):
    """Load products from database and update the table"""
    try:
        app.productos = app.producto_controller.get_all()
        update_productos_table(app)
    except Exception as e:
        print(f"Error loading products: {e}")

def update_productos_table(app):
    """Update the products table with current data"""
    app.productos_list.rows.clear()
    for producto in app.productos:
        # Calculate USD price from VES price
        rate = app.exchange_rate_service.get_dollar_rate()
        precio_usd = producto.precio / rate if rate else 0

        app.productos_list.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(producto.id))),
                    ft.DataCell(ft.Text(producto.nombre)),
                    ft.DataCell(ft.Text(f"${precio_usd:.2f}")),
                    ft.DataCell(ft.Text(f"Bs.{producto.precio:.2f}")),
                    ft.DataCell(ft.Text(str(producto.stock))),
                ],
                on_select_changed=lambda e, p=producto: on_row_selected(app, p)
            )
        )
    app.page.update()

def on_row_selected(app, producto):
    """Handle row selection in products table"""
    app.selected_producto = producto
    app.nombre.value = producto.nombre

    # Calculate USD price from VES price for editing
    rate = app.exchange_rate_service.get_dollar_rate()
    precio_usd = producto.precio / rate if rate else 0

    app.precio_usd.value = f"{precio_usd:.2f}"
    app.precio.value = str(producto.precio)
    app.stock.value = str(producto.stock)

    # Show edit buttons, hide add button
    app.add_button_container.visible = False
    app.edit_buttons_container.visible = True
    app.update_button.disabled = False
    app.delete_button.disabled = False

    app.page.update()

def add_producto(app, e):
    """Add a new product"""
    try:
        nombre = app.nombre.value.strip()
        precio = float(app.precio.value)
        stock = int(app.stock.value)

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        app.producto_controller.add_producto(nombre, precio, stock)
        clear_form(app)
        load_productos(app)

        app.page.snack_bar = ft.SnackBar(
            content=ft.Text("Producto agregado exitosamente"),
            bgcolor=ft.Colors.GREEN_600
        )
        app.page.snack_bar.open = True
        app.page.update()

    except ValueError as ex:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text(str(ex)),
            bgcolor=ft.Colors.RED_600
        )
        app.page.snack_bar.open = True
        app.page.update()
    except Exception as ex:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Error al agregar producto: {str(ex)}"),
            bgcolor=ft.Colors.RED_600
        )
        app.page.snack_bar.open = True
        app.page.update()

def update_producto(app, e):
    """Update selected product"""
    if not app.selected_producto:
        return

    try:
        nombre = app.nombre.value.strip()
        precio = float(app.precio.value)
        stock = int(app.stock.value)

        if not nombre:
            raise ValueError("El nombre es obligatorio")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        app.producto_controller.update_producto(app.selected_producto.id, nombre, precio, stock)
        clear_form(app)
        load_productos(app)

        app.page.snack_bar = ft.SnackBar(
            content=ft.Text("Producto actualizado exitosamente"),
            bgcolor=ft.Colors.GREEN_600
        )
        app.page.snack_bar.open = True
        app.page.update()

    except ValueError as ex:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text(str(ex)),
            bgcolor=ft.Colors.RED_600
        )
        app.page.snack_bar.open = True
        app.page.update()
    except Exception as ex:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Error al actualizar producto: {str(ex)}"),
            bgcolor=ft.Colors.RED_600
        )
        app.page.snack_bar.open = True
        app.page.update()

def delete_producto(app, e):
    """Delete selected product"""
    if not app.selected_producto:
        return

    try:
        app.producto_controller.delete_producto(app.selected_producto.id)
        clear_form(app)
        load_productos(app)

        app.page.snack_bar = ft.SnackBar(
            content=ft.Text("Producto eliminado exitosamente"),
            bgcolor=ft.Colors.GREEN_600
        )
        app.page.snack_bar.open = True
        app.page.update()

    except Exception as ex:
        app.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Error al eliminar producto: {str(ex)}"),
            bgcolor=ft.Colors.RED_600
        )
        app.page.snack_bar.open = True
        app.page.update()

def confirm_delete_producto(app, e):
    """Show confirmation dialog for product deletion"""
    if not app.selected_producto:
        return

    def delete_confirmed(e):
        app.page.dialog.open = False
        app.page.update()
        delete_producto(app, e)

    def cancel_delete(e):
        app.page.dialog.open = False
        app.page.update()

    app.page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Eliminación"),
        content=ft.Text(f"¿Está seguro de que desea eliminar el producto '{app.selected_producto.nombre}'?"),
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_delete),
            ft.ElevatedButton("Eliminar", on_click=delete_confirmed, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600))
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )
    app.page.dialog.open = True
    app.page.update()
    app.page.add(app.page.dialog)

def clear_form(app):
    """Clear the product form"""
    app.nombre.value = ""
    app.precio_usd.value = ""
    app.precio.value = ""
    app.stock.value = ""
    app.selected_producto = None

    # Show add button, hide edit buttons
    app.add_button_container.visible = True
    app.edit_buttons_container.visible = False
    app.update_button.disabled = True
    app.delete_button.disabled = True

    app.page.update()

def filter_productos(app, e):
    """Filter products based on search text"""
    search_text = app.search_field.value.lower().strip()
    if not search_text:
        # Show all products
        update_productos_table(app)
        return

    # Filter products
    filtered_products = [p for p in app.productos if search_text in p.nombre.lower()]
    app.productos_list.rows.clear()

    for producto in filtered_products:
        # Calculate USD price from VES price
        rate = app.exchange_rate_service.get_dollar_rate()
        precio_usd = producto.precio / rate if rate else 0

        app.productos_list.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(producto.id))),
                    ft.DataCell(ft.Text(producto.nombre)),
                    ft.DataCell(ft.Text(f"${precio_usd:.2f}")),
                    ft.DataCell(ft.Text(f"Bs.{producto.precio:.2f}")),
                    ft.DataCell(ft.Text(str(producto.stock))),
                ],
                on_select_changed=lambda e, p=producto: on_row_selected(app, p)
            )
        )
    app.page.update()

def update_precio_ves(app, e):
    """Update VES price when USD price changes"""
    try:
        precio_usd = float(app.precio_usd.value) if app.precio_usd.value else 0
        if precio_usd > 0:
            # Get exchange rate
            rate = app.exchange_rate_service.get_dollar_rate()
            if rate:
                precio_ves = precio_usd * rate
                app.precio.value = f"{precio_ves:.2f}"
            else:
                app.precio.value = ""
                app.page.snack_bar = ft.SnackBar(
                    content=ft.Text("No se pudo obtener la tasa de cambio del dólar"),
                    bgcolor=ft.Colors.ORANGE_600
                )
                app.page.snack_bar.open = True
        else:
            app.precio.value = ""
    except ValueError:
        app.precio.value = ""
    app.page.update()

def build_productos_view(app):
    # Campo de búsqueda
    app.search_field = ft.TextField(
        label="Buscar productos...",
        width=400,
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_productos(app, e),
        border_radius=10,
        height=50
    )

    # Campos del formulario con mejor diseño
    app.nombre = ft.TextField(
        label="Nombre del Producto",
        width=300,
        border_radius=10,
        height=50,
        prefix_icon=ft.Icons.SHOPPING_BAG
    )

    # Campo para precio en dólares
    app.precio_usd = ft.TextField(
        label="Precio (USD)",
        width=120,
        border_radius=10,
        height=50,
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_change=lambda e: update_precio_ves(app, e)
    )

    app.precio = ft.TextField(
        label="Precio (VES)",
        width=120,
        border_radius=10,
        height=50,
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER,
        read_only=True
    )
    app.stock = ft.TextField(
        label="Stock Inicial",
        width=120,
        border_radius=10,
        height=50,
        prefix_icon=ft.Icons.INVENTORY,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # Botones con mejor diseño
    app.add_button = ft.ElevatedButton(
        "Agregar Producto",
        on_click=app.add_producto,
        icon=ft.Icons.ADD,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=50,
        width=180
    )
    app.update_button = ft.ElevatedButton(
        "Actualizar Producto",
        on_click=app.update_producto,
        icon=ft.Icons.UPDATE,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=50,
        width=180,
        disabled=True
    )
    app.delete_button = ft.ElevatedButton(
        "Eliminar Producto",
        on_click=app.confirm_delete_producto,
        icon=ft.Icons.DELETE,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_600,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=50,
        width=180,
        disabled=True
    )

    app.productos_list = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio USD", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio VES", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        width=1100,
        border_radius=10,
        heading_row_height=50,
        data_row_min_height=45,
        data_row_max_height=60,
        heading_row_color=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800
    )

    # Crear contenedores para botones
    app.add_button_container = ft.Container(
        content=ft.Row(
            controls=[app.add_button],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        visible=True
    )
    app.edit_buttons_container = ft.Container(
        content=ft.Row(
            controls=[app.update_button, app.delete_button],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        visible=False
    )

    # Cargar productos después de crear la tabla
    app.load_productos()

    return ft.Column(
        controls=[
            # Título principal - movido a esquina superior izquierda
            ft.Container(
                content=ft.Text("Productos", size=32, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.top_left,
                padding=ft.padding.symmetric(vertical=10, horizontal=20)
            ),

            # Sección del formulario con botón a la derecha
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Información del Producto", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[
                                app.nombre,
                                app.precio_usd,
                                app.precio,
                                app.stock,
                                app.add_button
                            ],
                            spacing=15,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        app.edit_buttons_container
                    ],
                    spacing=15
                ),
                padding=20,
                bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=10,
                    color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26,
                    offset=ft.Offset(0, 2)
                )
            ),

            # Sección de lista con filtro dentro
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text("Lista de Productos", size=24, weight=ft.FontWeight.BOLD),
                                    ft.Container(width=20),  # Espacio entre texto y campo de búsqueda
                                    app.search_field
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=ft.padding.symmetric(horizontal=20, vertical=10)
                        ),
                        ft.Container(
                            content=ft.ListView(
                                controls=[app.productos_list],
                                height=370,
                                spacing=0,
                                padding=0
                            ),
                            height=370,
                            padding=20,
                            bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=10,
                                color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26,
                                offset=ft.Offset(0, 2)
                            )
                        )
                    ],
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                )
            )
        ],
        spacing=15,
        scroll=None  # Solo la lista tiene scroll
    )
