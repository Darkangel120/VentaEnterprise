import flet as ft
from datetime import datetime
from ..controllers.controllers import ProductoController, VentaController, FacturaController
from ..utils.exchange_rate import ExchangeRateService
from .ventas_view import build_ventas_view
from .productos_view import build_productos_view
from .factura_view import build_factura_view
from .reportes_view import build_reportes_view
from .dashboard_view import build_dashboard
import json
import os

class VentaEnterpriseApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "VentaEnterprise"

        # Crear carpeta oculta si no existe
        self.hidden_dir = ".ventaenterprise"
        os.makedirs(self.hidden_dir, exist_ok=True)
        import subprocess
        subprocess.run(['attrib', '+h', self.hidden_dir], shell=True)

        self.dark_mode = self.load_dark_mode_preference()
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT

        # Controllers
        self.producto_controller = ProductoController()
        self.venta_controller = VentaController()
        self.factura_controller = FacturaController()

        # Exchange rate service
        self.exchange_rate_service = ExchangeRateService(self.hidden_dir)
        self.exchange_rate = self.exchange_rate_service.get_dollar_rate()

        # Data
        self.productos = []
        self.carrito = []
        self.selected_producto = None
        self.selected_producto_venta = None

        # UI state
        self.current_view = "dashboard"
        self.last_click_time = None
        self.selected_cart_index = None
        self.cart_edit_mode = False
        self.cart_buttons_visible = False
        self.timer = None
        self.selected_index = 0

        # Initialize UI
        self.setup_ui()
        self.load_initial_data()

    def load_dark_mode_preference(self):
        """Load dark mode preference from a local file"""
        try:
            dark_mode_file = os.path.join(self.hidden_dir, "dark_mode_pref.json")
            if os.path.exists(dark_mode_file):
                with open(dark_mode_file, "r") as f:
                    data = json.load(f)
                    return data.get("dark_mode", False)
        except Exception as e:
            print(f"Error loading dark mode preference: {e}")
        return False

    def save_dark_mode_preference(self):
        """Save dark mode preference to a local file"""
        try:
            dark_mode_file = os.path.join(self.hidden_dir, "dark_mode_pref.json")
            with open(dark_mode_file, "w") as f:
                json.dump({"dark_mode": self.dark_mode}, f)
        except Exception as e:
            print(f"Error saving dark mode preference: {e}")

    def get_formatted_time(self):
        """Get formatted time"""
        return datetime.now().strftime('%H:%M')

    def get_formatted_date(self):
        """Get formatted date in Spanish"""
        now = datetime.now()
        day_names = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        month_names = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        day_name = day_names[now.weekday()]
        month_name = month_names[now.month - 1]
        return f"{now.day} de {month_name}, {day_name}"

    # Add missing methods for product actions
    def add_producto(self, e):
        from .productos_view import add_producto
        add_producto(self, e)

    def update_producto(self, e):
        from .productos_view import update_producto
        update_producto(self, e)

    def delete_producto(self, e):
        from .productos_view import delete_producto
        delete_producto(self, e)

    def confirm_delete_producto(self, e):
        from .productos_view import confirm_delete_producto
        confirm_delete_producto(self, e)

    def load_productos(self):
        from .productos_view import load_productos
        load_productos(self)

    def create_sidebar_item(self, index, icon, label):
        """Create a sidebar item with icon and text below"""
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=24),
                ft.Text(label, size=12, text_align=ft.TextAlign.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            bgcolor=ft.Colors.BLUE_100 if index == self.selected_index else None,
            padding=ft.padding.all(10),
            on_click=lambda e, idx=index: self.change_view(idx)
        )

    def setup_ui(self):
        # App Bar
        self.app_bar = ft.Container(
            content=ft.Row([
                ft.Row([
                    ft.Image(src="VP-logo.png", width=40, height=40),
                    ft.Text("VentaEnterprise", size=20, weight=ft.FontWeight.BOLD)
                ], spacing=5),
                ft.Text(f"💰 ${self.exchange_rate:.2f}" if self.exchange_rate else "💰 N/A", size=16),
                ft.Text(self.get_formatted_time(), size=16),
                ft.Text(self.get_formatted_date(), size=16),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.BLUE_600 if not self.dark_mode else ft.Colors.BLUE_900,
            padding=ft.padding.all(10),
            height=60
        )

        # Sidebar personalizado con iconos y texto debajo
        self.sidebar = ft.Container(
            content=ft.Column([
                self.create_sidebar_item(0, ft.Icons.DASHBOARD, "Dashboard"),
                self.create_sidebar_item(1, ft.Icons.SHOPPING_CART, "Ventas"),
                self.create_sidebar_item(2, ft.Icons.INVENTORY, "Productos"),
                self.create_sidebar_item(3, ft.Icons.RECEIPT, "Facturas"),
                self.create_sidebar_item(4, ft.Icons.ANALYTICS, "Reportes"),
                self.create_sidebar_item(5, ft.Icons.LIGHT_MODE if not self.dark_mode else ft.Icons.DARK_MODE, "Modo Oscuro" if self.dark_mode else "Modo Claro"),
            ], spacing=0),
            width=100,
            padding=ft.padding.all(10),
            bgcolor=ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900
        )

        # Main content area
        self.main_column = ft.Column(
            controls=[self.build_main_content()],
            expand=True
        )

        # Layout
        self.page.add(
            ft.Column([
                self.app_bar,
                ft.Row(
                    controls=[
                        self.sidebar,
                        ft.VerticalDivider(width=1),
                        self.main_column
                    ],
                    expand=True
                )
            ], expand=True)
        )

    def load_initial_data(self):
        """Load initial data for the application"""
        try:
            self.productos = self.producto_controller.get_all()
        except Exception as e:
            print(f"Error loading initial data: {e}")

    def change_view(self, index):
        """Change the current view based on navigation"""
        if index == 5:
            self.toggle_dark_mode()
        else:
            self.selected_index = index
            view_names = ["dashboard", "ventas", "productos", "facturas", "reportes"]
            self.current_view = view_names[index]
            self.main_column.controls[0] = self.build_main_content()
            self.update_sidebar_selection()
            self.page.update()

    def build_main_content(self):
        """Build the main content based on current view"""
        if self.current_view == "dashboard":
            return build_dashboard(self)
        elif self.current_view == "ventas":
            return build_ventas_view(self)
        elif self.current_view == "productos":
            return build_productos_view(self)
        elif self.current_view == "facturas":
            return build_factura_view(self)
        elif self.current_view == "reportes":
            return build_reportes_view(self)
        else:
            return ft.Text("Vista no encontrada")

    def toggle_dark_mode(self, e=None):
        """Toggle dark mode"""
        self.dark_mode = not self.dark_mode
        self.page.theme_mode = ft.ThemeMode.DARK if self.dark_mode else ft.ThemeMode.LIGHT
        # Update sidebar background
        self.sidebar.bgcolor = ft.Colors.BLUE_GREY_50 if not self.dark_mode else ft.Colors.BLUE_GREY_900
        # Update last sidebar item
        last_item = self.sidebar.content.controls[5]
        last_item.content.controls[0].name = ft.Icons.LIGHT_MODE if not self.dark_mode else ft.Icons.DARK_MODE
        last_item.content.controls[1].value = "Modo Oscuro" if self.dark_mode else "Modo Claro"
        self.app_bar.bgcolor = ft.Colors.BLUE_600 if not self.dark_mode else ft.Colors.BLUE_900
        self.main_column.controls[0] = self.build_main_content()
        self.save_dark_mode_preference()
        self.update_sidebar_selection()
        self.page.update()

    def toggle_sidebar(self, e):
        """Toggle sidebar extended/minimized"""
        self.sidebar_extended = not self.sidebar_extended
        self.navigation_rail.extended = self.sidebar_extended
        self.page.update()

    def setup_timer(self):
        """Setup timer for updating app bar"""
        self.timer = ft.Timer(interval=60, callback=self.update_app_bar)
        self.timer.start()

    def update_app_bar(self, e=None):
        """Update app bar with current time and dollar rate"""
        self.exchange_rate = self.exchange_rate_service.get_dollar_rate()
        dollar_text = f"💰 ${self.exchange_rate:.2f}" if self.exchange_rate else "💰 N/A"
        self.app_bar.content.controls[1].value = dollar_text
        self.app_bar.content.controls[2].value = self.get_formatted_time()
        self.app_bar.content.controls[3].value = self.get_formatted_date()
        self.page.update()

    def update_sidebar_selection(self):
        """Update sidebar item background based on selected index"""
        for i, item in enumerate(self.sidebar.content.controls):
            if i == self.selected_index:
                # Use a more visible color for dark mode
                item.bgcolor = ft.Colors.BLUE_300 if self.dark_mode else ft.Colors.BLUE_100
            else:
                item.bgcolor = None
        self.sidebar.update()

def main(page: ft.Page):
    app = VentaEnterpriseApp(page)

if __name__ == "__main__":
    ft.app(target=main)
