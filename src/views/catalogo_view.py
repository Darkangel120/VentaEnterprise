import flet as ft

def build_catalogo_view(app):
    # Campo de búsqueda para filtrar productos
    app.search_field = ft.TextField(
        label="Buscar productos...",
        width=400,
        border_radius=15,
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_800,
        prefix_icon=ft.Icons.SEARCH,
        on_change=app.filter_catalogo_products
    )

    # Botón para regresar a ventas
    back_button = ft.ElevatedButton(
        "Regresar a Ventas",
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda e: app.change_view("ventas"),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            padding=ft.padding.symmetric(horizontal=20, vertical=12)
        )
    )

    # Contenedor para la lista de productos filtrados
    app.product_list_container = ft.Container(
        content=create_productos_grid(app),
        height=650,  # Aumentado para mejor visualización
        alignment=ft.alignment.center
    )

    return ft.Column(
        controls=[
            # Header con título y botón de regreso
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("🛍️ Catálogo de Productos", size=32, weight=ft.FontWeight.BOLD),
                                ft.Text("Selecciona el producto que deseas vender", size=16, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                            ],
                            spacing=5,
                            expand=True
                        ),
                        back_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START
                ),
                padding=ft.padding.symmetric(vertical=20)
            ),

            # Barra de búsqueda
            ft.Container(
                content=app.search_field,
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            ),

            # Contenedor principal del catálogo
            ft.Container(
                content=ft.Column(
                    controls=[
                        app.product_list_container
                    ],
                    spacing=20
                ),
                padding=20,
                bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                border_radius=20,
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=15,
                    color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
                )
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO
    )

def create_productos_grid(app, productos_list=None):
    """Create a grid of product cards for selection"""
    productos = productos_list if productos_list is not None else app.productos

    if not productos:
        return ft.Container(
            content=ft.Text("No hay productos disponibles", size=16, color=ft.Colors.GREY),
            alignment=ft.alignment.center,
            height=200
        )

    product_cards = []
    for i, producto in enumerate(productos):
        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text("📦", size=32),
                        width=60,
                        height=60,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.BLUE_50 if not app.dark_mode else ft.Colors.BLUE_900,
                        border_radius=10
                    ),
                    ft.Text(producto.nombre, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text(f"${producto.precio:.2f}", size=18, color=ft.Colors.GREEN, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Stock: {producto.stock}", size=12, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=15,
            bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_800,
            border_radius=15,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
            ),
            on_click=lambda e, idx=i: app.select_product_for_sale(e, idx),
            height=180  # Altura fija para asegurar que el precio sea visible
        )
        product_cards.append(card)

    return ft.Container(
        content=ft.GridView(
            controls=product_cards,
            runs_count=4,
            max_extent=220,
            child_aspect_ratio=1.0,
            spacing=15,
            run_spacing=15,
            padding=10,
            # scroll=ft.ScrollMode.AUTO  # Eliminar scroll que causa error
        ),
        height=800  # Aumentada altura para mejor scroll y visibilidad
    )
