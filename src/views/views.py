import flet as ft
from datetime import datetime
from ..controllers.controllers import ProductoController, VentaController
from ..utils.exchange_rate import ExchangeRateService
from .ventas_view import build_ventas_view
from .productos_view import build_productos_view
from .catalogo_view import build_catalogo_view, create_productos_grid
from .factura_view import build_factura_view
from .reportes_view import build_reportes_view
from .dashboard_view import build_dashboard

class VentaEnterpriseApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "VentaEnterprise"
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()
        self.productos = []
        self.selected_producto = None
        self.carrito = []
        self.current_view = "dashboard"
        self.dark_mode = self.page.client_storage.get("dark_mode") or False
        self.sidebar_expanded = False
        self.exchange_rate = 1.0  # Default exchange rate
        self.selected_producto_venta = None

        # Variables para manejo del carrito
        self.selected_cart_index = None  # Índice del producto seleccionado en el carrito
        self.cart_edit_mode = False  # Si estamos en modo edición
        self.last_click_time = None  # Para detectar doble clic
        self.cart_buttons_visible = False  # Si los botones de eliminar/editar están visibles

        # Theme setup
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        self.page.update()

        # Load initial data
        self.load_productos()

        self.build_ui()

    def build_ui(self):
        self.page.vertical_alignment = ft.MainAxisAlignment.START

        # Main layout with navbar, sidebar and content
        self.main_column = ft.Column(
            controls=[
                self.build_navbar(),
                ft.Row(
                    controls=[
                        self.build_sidebar(),
                        ft.VerticalDivider(width=1),
                        ft.Container(
                            content=self.build_main_content(),
                            expand=True,
                            padding=20
                        )
                    ],
                    expand=True
                )
            ],
            expand=True
        )

        self.page.add(self.main_column)
        self.update_time_date()
        # Load initial exchange rate
        self.update_exchange_rate(None)

    def build_navbar(self):
        navbar_bg = ft.Colors.BLUE_600 if not self.dark_mode else ft.Colors.PURPLE_800
        return ft.Container(
            height=70,
            bgcolor=navbar_bg,  # Color azul/morado
            padding=ft.padding.symmetric(horizontal=0),  # Sin padding para ocupar todo el ancho
            margin=0,  # Sin margin para eliminar espacios feos
            content=ft.Row(
                controls=[
                    # Logo, title and menu button
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                ft.Icons.MENU,
                                icon_color=ft.Colors.WHITE,
                                tooltip="Toggle sidebar",
                                on_click=self.toggle_sidebar
                            ),
                            ft.Icon(
                                ft.Icons.STORE,
                                size=32,
                                color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                "VentaEnterprise",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START
                    ),

                    # Exchange rate display with refresh button
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "Tasa del Día",
                                            size=12,
                                            color=ft.Colors.BLUE_100
                                        ),
                                        ft.Text(
                                            "Cargando...",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.WHITE
                                        ),
                                    ],
                                    spacing=2,
                                    alignment=ft.MainAxisAlignment.START
                                ),
                                ft.IconButton(
                                    ft.Icons.REFRESH,
                                    icon_color=ft.Colors.WHITE,
                                    tooltip="Actualizar tasa de cambio",
                                    on_click=self.update_exchange_rate
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        bgcolor=navbar_bg,
                        border_radius=10
                    ),

                    # Time and Date - horizontal layout
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    "12:00 PM",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    "15 Septiembre",
                                    size=14,
                                    color=ft.Colors.BLUE_100
                                ),
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        bgcolor=navbar_bg,
                        border_radius=10
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )

    def build_sidebar(self):
        if self.sidebar_expanded:
            return ft.Container(
                width=250,
                bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                padding=20,
                content=ft.Column(
                    controls=[
                        # Navigation Menu - texto oculto si sidebar comprimido
                        ft.Column(
                            controls=[
                                self.create_nav_item("Dashboard", "dashboard", ft.Icons.DASHBOARD),
                                self.create_nav_item("Ventas", "ventas", ft.Icons.SHOPPING_CART),
                                self.create_nav_item("Productos", "productos", ft.Icons.INVENTORY),
                                self.create_nav_item("Factura", "factura", ft.Icons.RECEIPT),
                                self.create_nav_item("Reportes", "reportes", ft.Icons.ANALYTICS),
                            ],
                            spacing=5
                        ),
                        ft.Divider(height=20),

                        # Theme Toggle
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LIGHT_MODE if not self.dark_mode else ft.Icons.DARK_MODE,
                                        color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE
                                    ),
                                    ft.Switch(
                                        value=self.dark_mode,
                                        on_change=self.toggle_theme,
                                        active_color=ft.Colors.ORANGE
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=ft.padding.symmetric(vertical=10)
                        )
                    ],
                    spacing=10
                )
            )
        else:
            # Sidebar collapsed - solo iconos
            return ft.Container(
                width=60,
                bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                padding=ft.padding.symmetric(vertical=20),
                content=ft.Column(
                    controls=[
                        # Navigation Icons Only
                        ft.IconButton(
                            ft.Icons.DASHBOARD,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Dashboard",
                            on_click=lambda e: self.change_view("dashboard")
                        ),
                        ft.IconButton(
                            ft.Icons.SHOPPING_CART,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Ventas",
                            on_click=lambda e: self.change_view("ventas")
                        ),
                        ft.IconButton(
                            ft.Icons.INVENTORY,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Productos",
                            on_click=lambda e: self.change_view("productos")
                        ),
                        ft.IconButton(
                            ft.Icons.RECEIPT,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Factura",
                            on_click=lambda e: self.change_view("factura")
                        ),
                        ft.IconButton(
                            ft.Icons.ANALYTICS,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Reportes",
                            on_click=lambda e: self.change_view("reportes")
                        ),
                        ft.Divider(height=20),
                        # Theme Toggle Icon
                        ft.IconButton(
                            ft.Icons.LIGHT_MODE if not self.dark_mode else ft.Icons.DARK_MODE,
                            icon_color=ft.Colors.BLACK if not self.dark_mode else ft.Colors.WHITE,
                            tooltip="Cambiar tema",
                            on_click=self.toggle_theme
                        )
                    ],
                    spacing=15,
                    alignment=ft.MainAxisAlignment.START
                )
            )

    def create_nav_item(self, text, view_name, icon):
        is_selected = (self.current_view == view_name)
        text_color = ft.Colors.ORANGE if is_selected else (ft.Colors.WHITE if self.dark_mode else ft.Colors.BLACK)
        bg_color = ft.Colors.ORANGE_100 if is_selected and not self.dark_mode else (ft.Colors.ORANGE_900 if is_selected and self.dark_mode else ft.Colors.TRANSPARENT)
        return ft.Container(
            bgcolor=bg_color,
            padding=ft.padding.symmetric(vertical=8, horizontal=10),
            content=ft.Row(
                controls=[
                    ft.Icon(icon, size=20, color=text_color),
                    ft.Text(text, size=16, color=text_color) if self.sidebar_expanded else ft.Container(),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START
            ),
            on_click=lambda e: self.change_view(view_name),
            border_radius=10
        )

    def build_main_content(self):
        if self.current_view == "dashboard":
            return build_dashboard(self)
        elif self.current_view == "ventas":
            return build_ventas_view(self)
        elif self.current_view == "productos":
            return build_productos_view(self)
        elif self.current_view == "catalogo":
            return build_catalogo_view(self)
        elif self.current_view == "factura":
            return build_factura_view(self)
        elif self.current_view == "reportes":
            return build_reportes_view(self)
        else:
            return build_dashboard(self)

    def change_view(self, view_name):
        self.current_view = view_name
        # Validate view name, default to dashboard if invalid
        valid_views = ["dashboard", "ventas", "productos", "factura", "reportes", "catalogo"]
        if self.current_view not in valid_views:
            self.current_view = "dashboard"

        # Reload products when switching to products or catalog view
        if view_name == "productos" or view_name == "catalogo":
            self.load_productos()

        self.main_column.controls[1].controls[2].content = self.build_main_content()
        self.page.update()

    def toggle_theme(self, e):
        # Toggle dark mode
        self.dark_mode = not self.dark_mode
        self.page.client_storage.set("dark_mode", self.dark_mode)
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        self.main_column.controls[1].controls[0] = self.build_sidebar()
        self.main_column.controls[1].controls[2].content = self.build_main_content()
        self.page.update()

    def update_time_date(self):
        now = datetime.now()
        time_12h = now.strftime("%I:%M %p")
        day = now.day
        month_names = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agusto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        month_name = month_names[now.month - 1]
        date_str = f"{day} {month_name}"

        # Update navbar time and date - now in horizontal layout
        navbar = self.main_column.controls[0]
        time_container = navbar.content.controls[2]  # Time and date container (now at position 2)
        time_container.content.controls[0].value = time_12h  # Time text
        time_container.content.controls[1].value = date_str  # Date text
        self.page.update()

    def update_exchange_rate(self, e):
        try:
            exchange_service = ExchangeRateService()
            rate = exchange_service.get_dollar_rate()
            if rate and rate > 0:
                self.exchange_rate = rate  # Store the rate in instance variable
                # Update navbar exchange rate display
                navbar = self.main_column.controls[0]
                rate_container = navbar.content.controls[1]  # Exchange rate container (now at position 1)
                rate_container.content.controls[0].controls[1].value = f"1$ = {rate:.2f} BS"
                self.page.update()
            else:
                # Si no se pudo obtener la tasa, mostrar mensaje informativo
                navbar = self.main_column.controls[0]
                rate_container = navbar.content.controls[1]  # Exchange rate container (now at position 1)
                rate_container.content.controls[0].controls[1].value = "N/A"
                self.page.update()

                # Mostrar diálogo informativo en lugar de error
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("No se pudo obtener la tasa de cambio. Se usará la última tasa disponible o 1.0 por defecto."),
                    bgcolor=ft.Colors.ORANGE_600,
                    duration=4000
                )
                self.page.snack_bar.open = True
                self.page.update()

                # Usar tasa por defecto si no hay ninguna disponible
                if not self.exchange_rate or self.exchange_rate <= 0:
                    self.exchange_rate = 1.0

        except Exception as ex:
            print(f"Error actualizando tasa de cambio: {str(ex)}")
            # En caso de error, usar tasa por defecto
            if not self.exchange_rate or self.exchange_rate <= 0:
                self.exchange_rate = 1.0

            # Mostrar mensaje de error
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Error al actualizar la tasa de cambio. Usando valor por defecto."),
                bgcolor=ft.Colors.RED_600,
                duration=3000
            )
            self.page.snack_bar.open = True
            self.page.update()

    def toggle_sidebar(self, e):
        self.sidebar_expanded = not self.sidebar_expanded
        # Rebuild the sidebar to show/hide text labels
        self.main_column.controls[1].controls[0] = self.build_sidebar()
        self.page.update()

    def add_to_cart(self, e):
        if not hasattr(self, 'selected_producto_venta'):
            return
        try:
            cantidad = int(self.cantidad.value)
            if cantidad <= 0:
                raise ValueError("Cantidad debe ser positiva")
            if cantidad > self.selected_producto_venta.stock:
                raise ValueError("Stock insuficiente")
            self.carrito.append({
                'producto': self.selected_producto_venta,
                'cantidad': cantidad,
                'precio': self.selected_producto_venta.precio,
                'subtotal': cantidad * self.selected_producto_venta.precio
            })
            self.update_carrito()
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(str(ex)), actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())])
            self.page.dialog.open = True
            self.page.update()

    def select_cart_item(self, index):
        """Seleccionar un item del carrito para edición/eliminación"""
        if self.selected_cart_index == index:
            # Si ya está seleccionado, deseleccionar
            self.selected_cart_index = None
            self.cart_buttons_visible = False
        else:
            # Seleccionar nuevo item
            self.selected_cart_index = index
            self.cart_buttons_visible = True

        # Actualizar display del carrito
        self.update_carrito()

    def update_carrito(self):
        self.carrito_list.rows.clear()
        total = 0
        for i, item in enumerate(self.carrito):
            precio_ves = item['precio'] * self.exchange_rate
            subtotal_ves = item['subtotal'] * self.exchange_rate

            # Determinar si esta fila está seleccionada
            is_selected = (self.selected_cart_index == i)
            row_color = ft.Colors.BLUE_50 if is_selected and not self.dark_mode else (ft.Colors.BLUE_900 if is_selected and self.dark_mode else None)

            # Crear celdas con funcionalidad de edición si está en modo edición
            if self.cart_edit_mode and is_selected:
                # Modo edición: mostrar TextField para cantidad
                cantidad_cell = ft.DataCell(
                    ft.Container(
                        content=ft.TextField(
                            value=str(item['cantidad']),
                            width=80,
                            height=35,
                            text_align=ft.TextAlign.CENTER,
                            border_radius=5,
                            on_change=lambda e, idx=i: self.update_cart_quantity(idx, e.control.value),
                            on_submit=lambda e, idx=i: self.confirm_cart_edit(idx)
                        ),
                        alignment=ft.alignment.center
                    )
                )
            else:
                # Modo normal: mostrar texto
                cantidad_cell = ft.DataCell(ft.Text(str(item['cantidad'])))

            self.carrito_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['producto'].nombre)),
                        cantidad_cell,
                        ft.DataCell(ft.Text(f"{item['precio']:.2f}")),
                        ft.DataCell(ft.Text(f"{precio_ves:.2f}")),
                        ft.DataCell(ft.Text(f"{item['subtotal']:.2f}")),
                    ],
                    on_select_changed=lambda e, idx=i: self.handle_cart_click(idx),
                    color=row_color
                )
            )
            total += item['subtotal']
        total_ves = total * self.exchange_rate
        self.total_label.content.value = f"Total: ${total:.2f} / Bs.{total_ves:.2f}"
        self.page.update()

    def finalizar_venta(self, e):
        if not self.carrito:
            return
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = sum(item['subtotal'] for item in self.carrito)
        detalles = [{'producto_id': item['producto'].id, 'cantidad': item['cantidad'], 'precio': item['precio']} for item in self.carrito]
        self.venta_controller.registrar_venta(fecha, total, detalles)
        self.carrito.clear()
        self.update_carrito()
        self.page.dialog = ft.AlertDialog(title=ft.Text("Venta Finalizada"), content=ft.Text(f"Total: ${total:.2f}"), actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())])
        self.page.dialog.open = True
        self.page.update()

    def load_productos(self):
        self.productos = self.producto_controller.get_all()
        if hasattr(self, 'productos_list'):
            self.productos_list.rows.clear()
            for i, p in enumerate(self.productos):
                self.productos_list.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(p.id))),
                            ft.DataCell(ft.Text(p.nombre)),
                            ft.DataCell(ft.Text(f"{p.precio:.2f}")),
                            ft.DataCell(ft.Text(str(p.stock))),
                        ],
                        on_select_changed=lambda e, idx=i: self.on_row_selected(e, idx)
                    )
                )
            self.page.update()

    def on_row_selected(self, e, idx):
        if e.data == 'true':
            p = self.productos[idx]
            self.selected_producto = p
            self.nombre.value = p.nombre
            self.precio.value = str(p.precio)
            self.stock.value = str(p.stock)
            self.page.update()

    def add_producto(self, e):
        try:
            nombre = self.nombre.value.strip()
            precio = float(self.precio.value)
            stock = int(self.stock.value)
            if not nombre:
                raise ValueError("Nombre es obligatorio")
            self.producto_controller.add_producto(nombre, precio, stock)
            self.clear_form()
            self.load_productos()
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(str(ex)), actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())])
            self.page.dialog.open = True
            self.page.update()

    def update_producto(self, e):
        if not self.selected_producto:
            return
        try:
            nombre = self.nombre.value.strip()
            precio = float(self.precio.value)
            stock = int(self.stock.value)
            if not nombre:
                raise ValueError("Nombre es obligatorio")
            self.producto_controller.update_producto(self.selected_producto.id, nombre, precio, stock)
            self.clear_form()
            self.load_productos()
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(title=ft.Text("Error"), content=ft.Text(str(ex)), actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())])
            self.page.dialog.open = True
            self.page.update()

    def delete_producto(self, e):
        if not self.selected_producto:
            return
        self.producto_controller.delete_producto(self.selected_producto.id)
        self.clear_form()
        self.load_productos()

    def clear_form(self):
        self.nombre.value = ""
        self.precio.value = ""
        self.stock.value = ""
        self.selected_producto = None
        self.page.update()

    def select_product_for_sale(self, e, idx):
        """Handle product selection for sale"""
        self.selected_producto_venta = self.productos[idx]

        # Update the selected product display in the ventas view
        if hasattr(self, 'producto_seleccionado_text'):
            self.producto_seleccionado_text.value = f"Producto seleccionado: {self.selected_producto_venta.nombre}"

        # Enable quantity field since we have a selected product
        if hasattr(self, 'cantidad'):
            self.cantidad.disabled = False
            self.cantidad.value = "1"  # Reset to default quantity

        # Automatically return to ventas view
        self.change_view("ventas")

    def get_color_with_opacity(self, color, opacity):
        """Convertir un color de Flet a uno con opacidad"""
        # Extraer componentes RGB del color
        if color == ft.Colors.GREEN:
            return ft.Colors.GREEN_200
        elif color == ft.Colors.BLUE:
            return ft.Colors.BLUE_200
        elif color == ft.Colors.ORANGE:
            return ft.Colors.ORANGE_200
        elif color == ft.Colors.PURPLE:
            return ft.Colors.PURPLE_200
        elif color == ft.Colors.RED:
            return ft.Colors.RED_200
        elif color == ft.Colors.YELLOW:
            return ft.Colors.YELLOW_200
        elif color == ft.Colors.GREY:
            return ft.Colors.GREY_300
        elif color == ft.Colors.BLUE_GREY:
            return ft.Colors.BLUE_GREY_300
        else:
            return ft.Colors.BLUE_GREY_200  # Color por defecto

    def sort_table_by(self, criteria):
        """Sort the reportes table by the specified criteria"""
        try:
            estadisticas = self.venta_controller.get_estadisticas_reportes()

            if not estadisticas['productos_mas_vendidos']:
                return

            if criteria == "ventas":
                # Sort by sales quantity (descending)
                estadisticas['productos_mas_vendidos'].sort(key=lambda x: x[1], reverse=True)
            elif criteria == "ingresos":
                # Sort by revenue (descending)
                estadisticas['productos_mas_vendidos'].sort(key=lambda x: x[2], reverse=True)

            # Update the view with sorted data
            self.main_column.controls[1].controls[2].content = self.build_main_content()
            self.page.update()

            # Show success message
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Tabla ordenada por {criteria}"),
                bgcolor=ft.Colors.GREEN_600
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as e:
            print(f"Error sorting table: {e}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Error al ordenar la tabla"),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar.open = True
            self.page.update()

    def export_reportes_csv(self, e):
        """Export reportes data to CSV file"""
        try:
            import csv
            import os
            from datetime import datetime

            estadisticas = self.venta_controller.get_estadisticas_reportes()

            if not estadisticas['productos_mas_vendidos']:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("No hay datos para exportar"),
                    bgcolor=ft.Colors.ORANGE_600
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            # Create exports directory if it doesn't exist
            export_dir = "exports"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{export_dir}/reportes_ventas_{timestamp}.csv"

            # Write CSV file
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Producto', 'Ventas', 'Ingresos', 'Precio_Promedio', 'Stock_Restante', 'Porcentaje_Ventas', 'Porcentaje_Ingresos']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                total_ventas = sum(cantidad for _, cantidad, _ in estadisticas['productos_mas_vendidos'])
                total_ingresos = sum(ingresos for _, _, ingresos in estadisticas['productos_mas_vendidos'])

                for producto in estadisticas['productos_mas_vendidos']:
                    nombre, cantidad, ingresos = producto

                    # Get stock info
                    producto_info = next((p for p in self.productos if p.nombre == nombre), None)
                    stock_restante = producto_info.stock if producto_info else 0
                    precio_promedio = ingresos / cantidad if cantidad > 0 else 0

                    # Calculate percentages
                    porcentaje_ventas = (cantidad / total_ventas * 100) if total_ventas > 0 else 0
                    porcentaje_ingresos = (ingresos / total_ingresos * 100) if total_ingresos > 0 else 0

                    writer.writerow({
                        'Producto': nombre,
                        'Ventas': cantidad,
                        'Ingresos': f"{ingresos:.2f}",
                        'Precio_Promedio': f"{precio_promedio:.2f}",
                        'Stock_Restante': stock_restante,
                        'Porcentaje_Ventas': f"{porcentaje_ventas:.1f}%",
                        'Porcentaje_Ingresos': f"{porcentaje_ingresos:.1f}%"
                    })

                # Add summary row
                writer.writerow({})
                writer.writerow({
                    'Producto': 'TOTAL',
                    'Ventas': total_ventas,
                    'Ingresos': f"{total_ingresos:.2f}",
                    'Precio_Promedio': '',
                    'Stock_Restante': '',
                    'Porcentaje_Ventas': '100.0%',
                    'Porcentaje_Ingresos': '100.0%'
                })

            # Show success message with file path
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Archivo exportado: {filename}"),
                bgcolor=ft.Colors.GREEN_600,
                duration=5000
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as e:
            print(f"Error exporting CSV: {e}")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Error al exportar archivo CSV"),
                bgcolor=ft.Colors.RED_600
            )
            self.page.snack_bar.open = True
            self.page.update()

    def filter_catalogo_products(self, e):
        """Filter products in the catalog view based on search text"""
        if not hasattr(self, 'product_list_container'):
            return

        search_text = self.search_field.value.lower() if hasattr(self, 'search_field') and self.search_field.value else ""

        # Filter products
        filtered_products = [
            producto for producto in self.productos
            if search_text in producto.nombre.lower() and producto.stock > 0
        ]

        # Update the product list container with filtered products
        self.product_list_container.content = create_productos_grid(self, filtered_products)
        self.page.update()


def main(page: ft.Page):
    app = VentaEnterpriseApp(page)

if __name__ == "__main__":
    ft.app(target=main)