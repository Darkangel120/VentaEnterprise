import flet as ft

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
        on_click=lambda e: app.change_view("catalogo"),
        icon=ft.Icons.LIST,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )
    )

    app.aceptar_button = ft.ElevatedButton(
        "Aceptar",
        on_click=app.add_to_cart,
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
        on_click=app.editar_item_carrito,
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
        on_click=app.eliminar_item_carrito,
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
        on_click=app.finalizar_venta,
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
    app.productos_container = ft.Container()  # Will hold the modal or product list when opened

    # Poblar el carrito con los datos actuales
    app.update_carrito()

    return ft.Column(
        controls=[
            # Header
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("🛒 Sistema de Ventas", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Selecciona productos y gestiona tu carrito", size=16, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
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
                                spacing=15,
                                alignment=ft.MainAxisAlignment.START
                            ),
                            padding=ft.padding.symmetric(vertical=10)
                        ),
                    ],
                    spacing=15
                ),
                padding=20,
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
                        ft.Row(
                            controls=[
                                ft.Text("🛒 Carrito de Compras", size=24, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Text(f"{len(app.carrito)} items", size=14, color=ft.Colors.BLUE_GREY_600),
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                                    border_radius=15
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    app.carrito_list,
                                    ft.Divider(height=20),
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
                                spacing=20
                            ),
                            padding=20,
                            bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                            border_radius=15,
                            shadow=ft.BoxShadow(
                                spread_radius=1,
                                blur_radius=8,
                                color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
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
