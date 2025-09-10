import flet as ft

def build_factura_view(app):
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
                bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=10,
                height=400
            )
        ],
        spacing=20
    )