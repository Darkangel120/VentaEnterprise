import flet as ft

def build_productos_view(app):
    app.nombre = ft.TextField(label="Nombre del Producto", width=300)
    app.precio = ft.TextField(label="Precio", width=150)
    app.stock = ft.TextField(label="Stock Inicial", width=150)

    app.add_button = ft.ElevatedButton(
        "Agregar Producto",
        on_click=app.add_producto,
        icon=ft.Icons.ADD,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN)
    )
    app.update_button = ft.ElevatedButton(
        "Actualizar Producto",
        on_click=app.update_producto,
        icon=ft.Icons.UPDATE,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE)
    )
    app.delete_button = ft.ElevatedButton(
        "Eliminar Producto",
        on_click=app.delete_producto,
        icon=ft.Icons.DELETE,
        style=ft.ButtonStyle(bgcolor=ft.Colors.RED)
    )

    app.productos_list = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        width=1000,
        height=500,  # Aumentado para mejor visualización con muchos productos
        border_radius=10,
        heading_row_height=50,
        data_row_min_height=45,
        data_row_max_height=60,
        heading_row_color=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800
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
                            controls=[app.nombre, app.precio, app.stock],
                            spacing=20
                        ),
                        ft.Row(
                            controls=[app.add_button, app.update_button, app.delete_button],
                            spacing=20
                        ),
                    ],
                    spacing=15
                ),
                padding=20,
                bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=10
            ),

            ft.Divider(height=30),

            ft.Text("Lista de Productos", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=app.productos_list,
                padding=20,
                bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=10
            )
        ],
        spacing=20
    )
