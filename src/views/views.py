import flet as ft
from datetime import datetime
from ..controllers.controllers import ProductoController, VentaController
from ..utils.exchange_rate import ExchangeRateService

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

        # Theme setup
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        self.page.update()

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
            return self.build_dashboard()
        elif self.current_view == "ventas":
            return self.build_ventas_view()
        elif self.current_view == "productos":
            return self.build_productos_view()
        elif self.current_view == "factura":
            return self.build_factura_view()
        elif self.current_view == "reportes":
            return self.build_reportes_view()
        else:
            return self.build_dashboard()

    def build_dashboard(self):
        # Obtener datos reales de la base de datos
        ventas_dia = self.venta_controller.get_ventas_del_dia()
        productos_vendidos = self.venta_controller.get_productos_vendidos_hoy()
        clientes_atendidos = self.venta_controller.get_clientes_atendidos_hoy()
        valor_inventario = self.venta_controller.get_valor_inventario()

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header with gradient background
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Column(
                                            controls=[
                                                ft.Text("¡Bienvenido a VentaEnterprise!", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                                ft.Text("Dashboard Ejecutivo - Análisis de Ventas", size=16, color=ft.Colors.BLUE_100),
                                            ],
                                            spacing=8,
                                            alignment=ft.MainAxisAlignment.CENTER
                                        ),
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.DASHBOARD, size=64, color=ft.Colors.WHITE),
                                            alignment=ft.alignment.center
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ],
                            spacing=10
                        ),
                        padding=ft.padding.all(30),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.bottom_right,
                            colors=[ft.Colors.BLUE_700, ft.Colors.PURPLE_700] if not self.dark_mode else [ft.Colors.BLUE_900, ft.Colors.PURPLE_900]
                        ),
                        border_radius=ft.border_radius.only(bottom_left=20, bottom_right=20),
                        shadow=ft.BoxShadow(
                            spread_radius=2,
                            blur_radius=15,
                            color=ft.Colors.BLACK26
                        )
                    ),

                    # Quick Actions Bar
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    "Nueva Venta",
                                    icon=ft.Icons.ADD_SHOPPING_CART,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN_600,
                                        color=ft.Colors.WHITE,
                                        elevation=3
                                    ),
                                    on_click=lambda e: self.change_view("ventas")
                                ),
                                ft.ElevatedButton(
                                    "Agregar Producto",
                                    icon=ft.Icons.ADD_BOX,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.BLUE_600,
                                        color=ft.Colors.WHITE,
                                        elevation=3
                                    ),
                                    on_click=lambda e: self.change_view("productos")
                                ),
                                ft.ElevatedButton(
                                    "Ver Reportes",
                                    icon=ft.Icons.ANALYTICS,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.ORANGE_600,
                                        color=ft.Colors.WHITE,
                                        elevation=3
                                    ),
                                    on_click=lambda e: self.change_view("reportes")
                                ),
                            ],
                            spacing=15,
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=ft.padding.symmetric(vertical=20),
                        margin=ft.margin.symmetric(horizontal=20)
                    ),

                    # Enhanced Metrics Cards
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                self.create_professional_metric_card(
                                    "Ventas del Día", f"${ventas_dia:.2f}", ft.Colors.GREEN,
                                    ft.Icons.TRENDING_UP, "+18%", "vs ayer"
                                ),
                                self.create_professional_metric_card(
                                    "Productos Vendidos", str(productos_vendidos), ft.Colors.BLUE,
                                    ft.Icons.SHOPPING_BAG, "+12%", "esta semana"
                                ),
                                self.create_professional_metric_card(
                                    "Transacciones del Día", str(clientes_atendidos), ft.Colors.ORANGE,
                                    ft.Icons.RECEIPT, "+25%", "este mes"
                                ),
                                self.create_professional_metric_card(
                                    "Valor en Inventario", f"${valor_inventario:.2f}", ft.Colors.PURPLE,
                                    ft.Icons.INVENTORY, "+5%", "estimado"
                                ),
                            ],
                            spacing=20,
                            wrap=True,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                    ),

                    # Charts and Analytics Section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("📊 Análisis de Rendimiento", size=24, weight=ft.FontWeight.BOLD),
                                        ft.Container(
                                            content=ft.Text("Últimos 30 días", size=12, color=ft.Colors.BLUE_GREY_600),
                                            bgcolor=ft.Colors.BLUE_GREY_100 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
                                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                            border_radius=15
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Divider(height=20, thickness=2),

                                ft.Row(
                                    controls=[
                                        # Sales Trend Chart
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.Text("Tendencia de Ventas", size=18, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=self.create_sales_chart(),
                                    height=400,
                                    alignment=ft.alignment.center
                                )
                                                ],
                                                spacing=15
                                            ),
                                            expand=True,
                                            padding=25,
                                            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                                            border_radius=20,
                                            shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=12,
                                                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                                            )
                                        ),

                                        # Top Products & Quick Stats
                                        ft.Container(
                                            content=ft.Column(
                                                controls=[
                                                    ft.Text("🏆 Productos Destacados", size=18, weight=ft.FontWeight.BOLD),
                                                    ft.Column(
                                                        controls=self.create_top_products_list(),
                                                        spacing=12
                                                    ),

                                                    ft.Divider(height=20),

                                                    ft.Text("📈 Estadísticas Rápidas", size=16, weight=ft.FontWeight.BOLD),
                                                    ft.Column(
                                                        controls=self.create_quick_stats_list(),
                                                        spacing=8
                                                    )
                                                ],
                                                spacing=20
                                            ),
                                            width=350,
                                            padding=25,
                                            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                                            border_radius=20,
                                            shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=12,
                                                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                                            )
                                        )
                                    ],
                                    spacing=25,
                                    alignment=ft.MainAxisAlignment.START
                                )
                            ],
                            spacing=20
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                    ),

                    # Recent Activity Section
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Text("🕒 Actividad Reciente", size=24, weight=ft.FontWeight.BOLD),
                                        ft.Row(
                                            controls=[
                                                ft.ElevatedButton(
                                                    "Ver Todo",
                                                    icon=ft.Icons.ARROW_FORWARD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.BLUE_600,
                                                        color=ft.Colors.WHITE,
                                                        elevation=2
                                                    ),
                                                    on_click=lambda e: self.change_view("ventas")
                                                ),
                                                ft.ElevatedButton(
                                                    "Exportar",
                                                    icon=ft.Icons.DOWNLOAD,
                                                    style=ft.ButtonStyle(
                                                        bgcolor=ft.Colors.GREEN_600,
                                                        color=ft.Colors.WHITE,
                                                        elevation=2
                                                    )
                                                ),
                                            ],
                                            spacing=10
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),

                                ft.Container(
                                    content=ft.DataTable(
                                        columns=[
                                            ft.DataColumn(ft.Text("Hora", weight=ft.FontWeight.BOLD, size=14)),
                                            ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD, size=14)),
                                            ft.DataColumn(ft.Text("Productos", weight=ft.FontWeight.BOLD, size=14)),
                                            ft.DataColumn(ft.Text("Total", weight=ft.FontWeight.BOLD, size=14)),
                                            ft.DataColumn(ft.Text("Estado", weight=ft.FontWeight.BOLD, size=14)),
                                        ],
                                        rows=self.create_recent_activity_rows(),
                                        width=1000,
                                        height=300,
                                        border_radius=15,
                                        heading_row_height=50,
                                        data_row_min_height=50,
                                        heading_row_color=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_800
                                    ),
                                    padding=25,
                                    bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                                    border_radius=20,
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=12,
                                        color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                                    )
                                )
                            ],
                            spacing=20
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=10)
                    )
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO
            ),
            bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900
        )





    def create_productos_grid(self):
        """Create a grid of product cards for selection"""
        if not self.productos:
            return ft.Container(
                content=ft.Text("No hay productos disponibles", size=16, color=ft.Colors.GREY),
                alignment=ft.alignment.center,
                height=200
            )

        product_cards = []
        for i, producto in enumerate(self.productos):
            card = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text("📦", size=32),
                            width=60,
                            height=60,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BLUE_50 if not self.dark_mode else ft.Colors.BLUE_900,
                            border_radius=10
                        ),
                        ft.Text(producto.nombre, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"${producto.precio:.2f}", size=16, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Stock: {producto.stock}", size=12, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=15,
                bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_800,
                border_radius=15,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                ),
                on_click=lambda e, idx=i: self.select_product_for_sale(e, idx)
            )
            product_cards.append(card)

        return ft.GridView(
            controls=product_cards,
            runs_count=4,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=10
        )

    def select_product_for_sale(self, e, idx):
        """Handle product selection for sale"""
        self.selected_producto_venta = self.productos[idx]
        # Update the selected product display in the ventas view
        if hasattr(self, 'productos_container'):
            # Find the product selection container and update the text
            selection_container = self.productos_container.content.controls[0]  # The main container
            if len(selection_container.content.controls) > 1:
                product_display = selection_container.content.controls[1].content.controls[0]  # The row with product display
                product_display.controls[0].content.value = f"Producto seleccionado: {self.selected_producto_venta.nombre}"
                self.page.update()

    def change_view(self, view_name):
        self.current_view = view_name
        # Validate view name, default to dashboard if invalid
        valid_views = ["dashboard", "ventas", "productos", "factura", "reportes"]
        if self.current_view not in valid_views:
            self.current_view = "dashboard"
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
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
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
            if rate:
                # Update navbar exchange rate display
                navbar = self.main_column.controls[0]
                rate_container = navbar.content.controls[1]  # Exchange rate container (now at position 1)
                rate_container.content.controls[1].value = f"{rate:.2f}"
                self.page.update()
            else:
                raise Exception("No se pudo obtener la tasa de cambio")
        except Exception as ex:
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Error"),
                content=ft.Text(f"No se pudo actualizar la tasa de cambio: {str(ex)}"),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.page.dialog.close())]
            )
            self.page.dialog.open = True
            self.page.update()

    def toggle_sidebar(self, e):
        self.sidebar_expanded = not self.sidebar_expanded
        # Rebuild the sidebar to show/hide text labels
        self.main_column.controls[1].controls[0] = self.build_sidebar()
        self.page.update()

    def build_ventas_view(self):
        # Initialize form fields
        self.cantidad = ft.TextField(
            label="Cantidad",
            value="1",
            width=150,
            border_radius=10,
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_800
        )

        self.add_to_cart_button = ft.ElevatedButton(
            "Agregar al Carrito",
            on_click=self.add_to_cart,
            icon=ft.Icons.ADD_SHOPPING_CART,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=20, vertical=12)
            )
        )

        # Enhanced product selection with cards
        self.productos_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Catálogo de Productos", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.create_productos_grid(),
                        height=300,
                        padding=10,
                        bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                        border_radius=15
                    )
                ],
                spacing=15
            ),
            padding=20,
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
            )
        )

        # Enhanced cart display
        self.carrito_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cantidad", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Subtotal", weight=ft.FontWeight.BOLD)),
            ],
            rows=[],
            width=900,
            height=250,
            border_radius=10,
            heading_row_height=50,
        data_row_min_height=45
        )

        self.total_label = ft.Container(
            content=ft.Text("Total: $0.00", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.Colors.GREEN_50 if not self.dark_mode else ft.Colors.GREEN_900,
            border_radius=15
        )

        self.finalizar_venta_button = ft.ElevatedButton(
            "Finalizar Venta",
            on_click=self.finalizar_venta,
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                padding=ft.padding.symmetric(horizontal=30, vertical=15)
            )
        )

        return ft.Column(
            controls=[
                # Header
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("🛒 Sistema de Ventas", size=32, weight=ft.FontWeight.BOLD),
                            ft.Text("Selecciona productos y gestiona tu carrito", size=16, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                        ],
                        spacing=5
                    ),
                    padding=ft.padding.only(bottom=10)
                ),

                # Product Selection Section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Seleccionar Producto", size=20, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Text("Producto seleccionado: Ninguno", size=14),
                                            padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                            bgcolor=ft.Colors.BLUE_GREY_100 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
                                            border_radius=10,
                                            expand=True
                                        ),
                                        self.cantidad,
                                        self.add_to_cart_button
                                    ],
                                    spacing=15,
                                    alignment=ft.MainAxisAlignment.START
                                ),
                                padding=ft.padding.symmetric(vertical=10)
                            ),
                        ],
                        spacing=15
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=15,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                    )
                ),

                # Products Grid
                self.productos_container,

                # Cart Section
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Text("🛒 Carrito de Compras", size=24, weight=ft.FontWeight.BOLD),
                                    ft.Container(
                                        content=ft.Text("0 items", size=14, color=ft.Colors.BLUE_GREY_600),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        bgcolor=ft.Colors.BLUE_GREY_100 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
                                        border_radius=15
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        self.carrito_list,
                                        ft.Divider(height=20),
                                        ft.Row(
                                            controls=[
                                                self.total_label,
                                                self.finalizar_venta_button
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                                        )
                                    ],
                                    spacing=20
                                ),
                                padding=20,
                                bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                                border_radius=15,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=8,
                                    color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
                                )
                            )
                        ],
                        spacing=20
                    ),
                    padding=ft.padding.symmetric(vertical=10)
                )
            ],
            spacing=30,
            scroll=ft.ScrollMode.AUTO
        )

    def build_productos_view(self):
        self.nombre = ft.TextField(label="Nombre del Producto", width=300)
        self.precio = ft.TextField(label="Precio", width=150)
        self.stock = ft.TextField(label="Stock Inicial", width=150)

        self.add_button = ft.ElevatedButton(
            "Agregar Producto",
            on_click=self.add_producto,
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN)
        )
        self.update_button = ft.ElevatedButton(
            "Actualizar Producto",
            on_click=self.update_producto,
            icon=ft.Icons.UPDATE,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)
        )
        self.delete_button = ft.ElevatedButton(
            "Eliminar Producto",
            on_click=self.delete_producto,
            icon=ft.Icons.DELETE,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED)
        )

        self.productos_list = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Precio")),
                ft.DataColumn(ft.Text("Stock")),
            ],
            rows=[],
            width=1000,
            height=400,
        )

        return ft.Column(
            controls=[
                ft.Text("Gestión de Productos", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Información del Producto", size=18, weight=ft.FontWeight.BOLD),
                            ft.Row(
                                controls=[self.nombre, self.precio, self.stock],
                                spacing=20
                            ),
                            ft.Row(
                                controls=[self.add_button, self.update_button, self.delete_button],
                                spacing=20
                            ),
                        ],
                        spacing=15
                    ),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=10
                ),

                ft.Divider(height=30),

                ft.Text("Lista de Productos", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.productos_list,
                    padding=20,
                    bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=10
                )
            ],
            spacing=20
        )

    def build_factura_view(self):
        return ft.Column(
            controls=[
                ft.Text("Sistema de Facturación", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("Factura Actual", size=24, weight=ft.FontWeight.BOLD),
                            ft.Text("No hay factura activa", size=18, color=ft.Colors.GREY),
                            ft.ElevatedButton(
                                "Generar Nueva Factura",
                                icon=ft.Icons.RECEIPT_LONG,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)
                            )
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    padding=40,
                    bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=10,
                    height=400
                )
            ],
            spacing=20
        )

    def build_reportes_view(self):
        # Obtener datos reales de la base de datos
        estadisticas = self.venta_controller.get_estadisticas_reportes()

        # Crear métricas dinámicas
        metricas = []

        if estadisticas['productos_mas_vendidos']:
            producto_top = estadisticas['productos_mas_vendidos'][0]
            metricas.append(self.create_metric_card(
                "Producto Más Vendido",
                producto_top[0],  # nombre del producto
                ft.Colors.GREEN,
                ft.Icons.STAR
            ))
        else:
            metricas.append(self.create_metric_card(
                "Producto Más Vendido",
                "Sin datos",
                ft.Colors.GREY,
                ft.Icons.STAR
            ))

        metricas.append(self.create_metric_card(
            "Total de Ventas",
            str(estadisticas['total_ventas']),
            ft.Colors.BLUE,
            ft.Icons.SHOPPING_CART
        ))

        metricas.append(self.create_metric_card(
            "Promedio por Venta",
            f"${estadisticas['promedio_venta']:.2f}",
            ft.Colors.PURPLE,
            ft.Icons.ATTACH_MONEY
        ))

        # Crear filas de la tabla de análisis
        table_rows = []
        if estadisticas['productos_mas_vendidos']:
            for producto in estadisticas['productos_mas_vendidos']:
                nombre, cantidad, ingresos = producto
                # Obtener stock restante del producto
                producto_info = next((p for p in self.productos if p.nombre == nombre), None)
                stock_restante = producto_info.stock if producto_info else 0

                table_rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(nombre)),
                    ft.DataCell(ft.Text(str(cantidad))),
                    ft.DataCell(ft.Text(f"${ingresos:.2f}")),
                    ft.DataCell(ft.Text(str(stock_restante))),
                ]))
        else:
            table_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text("No hay datos de ventas", col=4)),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
                ft.DataCell(ft.Text("")),
            ]))

        return ft.Column(
            controls=[
                ft.Text("Reportes Detallados", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),

                ft.Row(
                    controls=metricas,
                    spacing=20
                ),

                ft.Divider(height=30),

                ft.Text("Análisis de Ventas", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Producto")),
                            ft.DataColumn(ft.Text("Ventas")),
                            ft.DataColumn(ft.Text("Ingresos")),
                            ft.DataColumn(ft.Text("Stock Restante")),
                        ],
                        rows=table_rows,
                        width=800,
                        height=300
                    ),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900,
                    border_radius=10
                )
            ],
            spacing=20
        )

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

    def update_carrito(self):
        self.carrito_list.rows.clear()
        total = 0
        for item in self.carrito:
            self.carrito_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item['producto'].nombre)),
                        ft.DataCell(ft.Text(str(item['cantidad']))),
                        ft.DataCell(ft.Text(f"{item['precio']:.2f}")),
                        ft.DataCell(ft.Text(f"{item['subtotal']:.2f}")),
                    ]
                )
            )
            total += item['subtotal']
        self.total_label.value = f"Total: ${total:.2f}"
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

    def create_professional_metric_card(self, title, value, color, icon, trend, subtitle):
        # Crear color de fondo con opacidad correcta
        bg_color = self.get_color_with_opacity(color, 0.2)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(icon, size=36, color=color),
                                width=50,
                                height=50,
                                alignment=ft.alignment.center,
                                bgcolor=bg_color,
                                border_radius=12
                            ),
                            ft.Container(
                                content=ft.Text(trend, size=11, color=ft.Colors.GREEN if trend.startswith('+') else ft.Colors.RED, weight=ft.FontWeight.BOLD),
                                bgcolor=ft.Colors.GREEN_100 if trend.startswith('+') else ft.Colors.RED_100,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=12
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Text(title, size=13, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(subtitle, size=10, color=ft.Colors.BLUE_GREY_500 if not self.dark_mode else ft.Colors.BLUE_GREY_500),
                ],
                spacing=6
            ),
            width=300,
            height=150,
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
            )
        )

    def create_sales_chart(self):
        """Create an enhanced sales chart with real data from database"""
        # Obtener datos reales de ventas de los últimos 7 días
        datos_ventas = self.venta_controller.get_datos_grafico_ventas(dias=7)

        # Calcular estadísticas
        total_semana = sum(datos_ventas)
        promedio_diario = total_semana / len(datos_ventas) if datos_ventas else 0
        max_venta = max(datos_ventas) if datos_ventas else 0
        mejor_dia_idx = datos_ventas.index(max_venta) if datos_ventas and max_venta > 0 else 0

        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        mejor_dia = dias_semana[mejor_dia_idx] if datos_ventas else "N/A"

        # Calcular altura máxima para las barras (normalizar)
        max_altura = 150
        max_valor = max(datos_ventas) if datos_ventas else 1

        # Crear barras del gráfico
        barras = []
        colores = [ft.Colors.BLUE_500, ft.Colors.BLUE_600, ft.Colors.BLUE_500,
                  ft.Colors.BLUE_700, ft.Colors.BLUE_600, ft.Colors.BLUE_700, ft.Colors.BLUE_500]

        for i, (dia, valor) in enumerate(zip(dias_semana, datos_ventas)):
            altura = int((valor / max_valor) * max_altura) if max_valor > 0 else 0
            barras.append(self.create_enhanced_bar(dia, valor, altura, colores[i]))

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Header with title and summary
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text("📈 Análisis de Ventas Detallado", size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text("Tendencia semanal con métricas clave", size=12, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.START,
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text(f"${total_semana:.2f}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                                        ft.Text("Total Semana", size=10, color=ft.Colors.BLUE_GREY_500),
                                    ],
                                    spacing=2,
                                    alignment=ft.MainAxisAlignment.END
                                ),
                                padding=ft.padding.symmetric(horizontal=15, vertical=8),
                                bgcolor=ft.Colors.GREEN_50 if not self.dark_mode else ft.Colors.GREEN_900,
                                border_radius=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Divider(height=15),
                    # Enhanced chart with multiple metrics
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Sales bars with values
                                ft.Container(
                                    content=ft.Row(
                                        controls=barras,
                                        spacing=12,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    height=200,
                                    alignment=ft.alignment.center
                                ),
                                # Trend indicators
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[
                                                        ft.Icon(ft.Icons.TRENDING_UP, size=16, color=ft.Colors.GREEN),
                                                        ft.Text("+18.5%", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                                                        ft.Text("vs semana anterior", size=10, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                                                    ],
                                                    spacing=5,
                                                    alignment=ft.MainAxisAlignment.START
                                                ),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                                bgcolor=ft.Colors.GREEN_50 if not self.dark_mode else ft.Colors.GREEN_900,
                                                border_radius=15
                                            ),
                                            ft.Container(
                                                content=ft.Row(
                                                    controls=[
                                                        ft.Icon(ft.Icons.STAR, size=16, color=ft.Colors.ORANGE),
                                                        ft.Text(f"{mejor_dia} pico", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                                                        ft.Text(f"${max_venta:.2f}", size=10, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                                                    ],
                                                    spacing=5,
                                                    alignment=ft.MainAxisAlignment.START
                                                ),
                                                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                                bgcolor=ft.Colors.ORANGE_50 if not self.dark_mode else ft.Colors.ORANGE_900,
                                                border_radius=15
                                            ),
                                        ],
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    ),
                                    padding=ft.padding.symmetric(vertical=10)
                                ),
                                # Additional metrics row
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            self.create_mini_metric("Promedio Diario", f"${promedio_diario:.2f}", ft.Colors.BLUE),
                                            self.create_mini_metric("Mejor Día", mejor_dia, ft.Colors.GREEN),
                                            self.create_mini_metric("Transacciones", str(sum(1 for v in datos_ventas if v > 0)), ft.Colors.PURPLE),
                                        ],
                                        spacing=15,
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND
                                    ),
                                    padding=ft.padding.symmetric(vertical=10)
                                )
                            ],
                            spacing=15
                        ),
                        height=280,
                        alignment=ft.alignment.center
                    )
                ],
                spacing=15
            ),
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
            border_radius=15,
            padding=ft.padding.all(20)
        )

    def create_enhanced_bar(self, day, amount, height, color):
        """Create an enhanced bar with value display"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Value display above bar
                    ft.Container(
                        content=ft.Text(f"${amount}", size=10, weight=ft.FontWeight.BOLD, color=color),
                        height=20,
                        alignment=ft.alignment.center
                    ),
                    # The bar itself
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    height=height,
                                    width=25,
                                    bgcolor=color,
                                    border_radius=ft.border_radius.only(top_left=4, top_right=4),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=4,
                                        color=ft.Colors.BLUE_200
                                    )
                                ),
                                # Base of the bar
                                ft.Container(
                                    height=5,
                                    width=35,
                                    bgcolor=ft.Colors.BLUE_300,
                                    border_radius=ft.border_radius.only(bottom_left=6, bottom_right=6)
                                )
                            ],
                            spacing=0,
                            alignment=ft.MainAxisAlignment.END
                        ),
                        height=height + 5,
                        alignment=ft.alignment.bottom_center
                    ),
                    # Day label
                    ft.Container(
                        content=ft.Text(day, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_700 if not self.dark_mode else ft.Colors.BLUE_GREY_300),
                        height=25,
                        alignment=ft.alignment.center
                    )
                ],
                spacing=2,
                alignment=ft.MainAxisAlignment.END
            ),
            height=height + 50,
            alignment=ft.alignment.bottom_center
        )

    def create_mini_metric(self, label, value, color):
        """Create a mini metric display"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(label, size=11, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=3,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
            border_radius=12,
            width=100
        )

    def create_top_products_list(self):
        """Create a list of top products from database"""
        try:
            # Obtener productos más vendidos de la base de datos
            top_products = self.venta_controller.get_productos_mas_vendidos(limit=4)

            if not top_products:
                return [
                    ft.Text("No hay datos de ventas disponibles", size=14, color=ft.Colors.GREY)
                ]

            product_items = []
            medal_colors = [ft.Colors.YELLOW, ft.Colors.GREY, ft.Colors.ORANGE, ft.Colors.BLUE_GREY]

            for i, product in enumerate(top_products):
                medal_color = medal_colors[i] if i < len(medal_colors) else ft.Colors.BLUE_GREY
                item = self.create_top_product_item_pro(
                    product['nombre'],
                    f"${product['precio']:.2f}",
                    f"{product['ventas']} ventas",
                    medal_color
                )
                product_items.append(item)

            return product_items

        except Exception as e:
            print(f"Error al obtener productos destacados: {e}")
            return [
                ft.Text("Error al cargar productos destacados", size=14, color=ft.Colors.RED)
            ]

    def create_top_product_item_pro(self, name, price, sales, medal_color):
        # Crear color de fondo con opacidad correcta
        bg_color = self.get_color_with_opacity(medal_color, 0.2)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.EMOJI_EVENTS, size=24, color=medal_color),
                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                        bgcolor=bg_color,
                        border_radius=20
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(name, size=14, weight=ft.FontWeight.BOLD),
                            ft.Text(price, size=12, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=2,
                        alignment=ft.MainAxisAlignment.START,
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(sales, size=12, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                        bgcolor=ft.Colors.BLUE_GREY_100 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
                        border_radius=15
                    )
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=ft.padding.symmetric(horizontal=15, vertical=12),
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_800,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=6,
                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
            )
        )

    def create_quick_stats_list(self):
        """Create a list of quick statistics"""
        try:
            # Get some basic statistics
            ventas_dia = self.venta_controller.get_ventas_del_dia()
            productos_vendidos = self.venta_controller.get_productos_vendidos_hoy()
            clientes_atendidos = self.venta_controller.get_clientes_atendidos_hoy()

            return [
                self.create_quick_stat("Ventas Hoy", f"${ventas_dia:.2f}", ft.Colors.GREEN),
                self.create_quick_stat("Productos Vendidos", str(productos_vendidos), ft.Colors.BLUE),
                self.create_quick_stat("Transacciones Hoy", str(clientes_atendidos), ft.Colors.ORANGE),
            ]
        except Exception as e:
            print(f"Error al obtener estadísticas rápidas: {e}")
            return [
                self.create_quick_stat("Error", "No disponible", ft.Colors.RED),
            ]

    def create_quick_stat(self, label, value, color):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(label, size=12, color=ft.Colors.BLUE_GREY_600 if not self.dark_mode else ft.Colors.BLUE_GREY_400),
                    ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_800,
            border_radius=10
        )

    def create_status_badge(self, status, color):
        return ft.Container(
            content=ft.Text(status, size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            bgcolor=color,
            border_radius=12
        )

    def create_recent_activity_rows(self):
        """Create recent activity rows from database"""
        try:
            # Obtener ventas recientes de la base de datos
            ventas_recientes = self.venta_controller.get_ventas_recientes(limit=4)

            if not ventas_recientes:
                return [
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text("--:--", size=13)),
                        ft.DataCell(ft.Text("Sin ventas recientes", size=13)),
                        ft.DataCell(ft.Text("0 items", size=13)),
                        ft.DataCell(ft.Text("$0.00", color=ft.Colors.GREY, weight=ft.FontWeight.BOLD, size=13)),
                        ft.DataCell(self.create_status_badge("Sin datos", ft.Colors.GREY)),
                    ])
                ]

            rows = []
            for venta in ventas_recientes:
                # Formatear la hora
                hora = venta['fecha'].strftime("%H:%M") if hasattr(venta['fecha'], 'strftime') else str(venta['fecha'])

                # Obtener información del cliente (usando un nombre genérico si no hay cliente específico)
                cliente = venta.get('cliente', 'Cliente Anónimo')

                # Calcular cantidad total de productos
                cantidad_total = sum(detalle['cantidad'] for detalle in venta.get('detalles', []))

                # Estado de la venta
                estado = "Completada"
                estado_color = ft.Colors.GREEN

                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(hora, size=13)),
                    ft.DataCell(ft.Text(cliente, size=13)),
                    ft.DataCell(ft.Text(f"{cantidad_total} items", size=13)),
                    ft.DataCell(ft.Text(f"${venta['total']:.2f}", color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD, size=13)),
                    ft.DataCell(self.create_status_badge(estado, estado_color)),
                ])
                rows.append(row)

            return rows

        except Exception as e:
            print(f"Error al obtener actividad reciente: {e}")
            return [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("--:--", size=13)),
                    ft.DataCell(ft.Text("Error al cargar", size=13)),
                    ft.DataCell(ft.Text("0 items", size=13)),
                    ft.DataCell(ft.Text("$0.00", color=ft.Colors.RED, weight=ft.FontWeight.BOLD, size=13)),
                    ft.DataCell(self.create_status_badge("Error", ft.Colors.RED)),
                ])
            ]

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

    def create_metric_card(self, title, value, color, icon):
        # Crear color de fondo con opacidad correcta
        bg_color = self.get_color_with_opacity(color, 0.2)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, size=40, color=color),
                        width=60,
                        height=60,
                        alignment=ft.alignment.center,
                        bgcolor=bg_color,
                        border_radius=15
                    ),
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color, text_align=ft.TextAlign.CENTER),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=320,
            height=160,
            padding=ft.padding.all(20),
            bgcolor=ft.Colors.WHITE if not self.dark_mode else ft.Colors.BLUE_GREY_900,
            border_radius=20,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=12,
                color=ft.Colors.BLACK12 if not self.dark_mode else ft.Colors.BLACK26
            )
        )


def main(page: ft.Page):
    app = VentaEnterpriseApp(page)

if __name__ == "__main__":
    ft.app(target=main)
