import flet as ft

def build_productos_view(app):
    # Campo de búsqueda
    app.search_field = ft.TextField(
        label="Buscar productos...",
        width=400,
        prefix_icon=ft.Icons.SEARCH,
        on_change=app.filter_productos,
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
    app.precio = ft.TextField(
        label="Precio (VES)",
        width=150,
        border_radius=10,
        height=50,
        prefix_icon=ft.Icons.ATTACH_MONEY,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    app.stock = ft.TextField(
        label="Stock Inicial",
        width=150,
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
            # Título principal
            ft.Container(
                content=ft.Text("Gestión de Productos", size=32, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=ft.padding.symmetric(vertical=10)
            ),
            ft.Divider(height=20),

            # Sección del formulario
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Información del Producto", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            controls=[app.nombre, app.precio, app.stock],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        app.add_button_container,
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

            ft.Divider(height=30),

            # Sección de búsqueda y lista
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Lista de Productos", size=24, weight=ft.FontWeight.BOLD),
                                app.search_field
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Container(
                            content=app.productos_list,
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
                    spacing=15
                )
            )
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO
    )
