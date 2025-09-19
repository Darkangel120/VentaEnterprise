import flet as ft
from datetime import datetime
from ..controllers.controllers import FacturaController

factura_controller = FacturaController()

def build_factura_view(app):
    # Initialize UI components following ventas_view pattern
    app.facturas_list = []
    app.selected_factura = None
    app.facturas_search_text = ""

    # Search field
    app.facturas_search_field = ft.TextField(
        label="Buscar facturas...",
        prefix_icon=ft.Icons.SEARCH,
        width=300,
        border_radius=10,
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_800,
        on_change=lambda e: filtrar_facturas(app)
    )

    # Facturas grid
    app.facturas_grid = ft.GridView(
        runs_count=3,
        max_extent=400,
        child_aspect_ratio=1.5,
        spacing=10,
        run_spacing=10,
        height=600
    )

    def load_facturas():
        """Cargar lista de facturas"""
        app.facturas_list = factura_controller.get_all()
        filtrar_facturas(app)

    def filtrar_facturas(app_instance):
        """Filtrar facturas según búsqueda"""
        search_text = app.facturas_search_field.value.lower() if app.facturas_search_field.value else ""
        app_instance.facturas_search_text = search_text

        facturas_filtradas = []
        for f in app_instance.facturas_list:
            # Filtro por búsqueda (ID o nombres de productos)
            if search_text:
                encontrado = search_text in str(f.id).lower()
                if not encontrado:
                    for detalle in f.detalles:
                        if search_text in detalle['nombre'].lower():
                            encontrado = True
                            break
                if not encontrado:
                    continue
            facturas_filtradas.append(f)

        # Deseleccionar si la factura seleccionada no está en la lista filtrada
        if app_instance.selected_factura and app_instance.selected_factura not in facturas_filtradas:
            app_instance.selected_factura = None

        update_facturas_grid(app_instance, facturas_filtradas)

    def update_facturas_grid(app_instance, facturas_list):
        """Actualizar el grid de facturas"""
        app.facturas_grid.controls.clear()

        for f in facturas_list:
            # Determinar si esta factura está seleccionada
            is_selected = (app_instance.selected_factura and app_instance.selected_factura.id == f.id)
            card_bgcolor = ft.Colors.BLUE_GREY_800 if app.dark_mode else ft.Colors.WHITE

            def on_ver_detalles(e):
                if app_instance.selected_factura:
                    mostrar_dialogo_factura(app_instance, app_instance.selected_factura)

            # Crear card moderna para cada factura con mejor diseño
            card = ft.Card(
                content=ft.Container(
                    content=ft.Stack([
                        # Contenido principal de la tarjeta
                        ft.Column([
                            # Encabezado con ID y icono
                            ft.Container(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.RECEIPT, size=24, color=ft.Colors.BLUE_600),
                                    ft.Text(f"Factura #{f.id:04d}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                                padding=ft.padding.symmetric(vertical=10),
                                bgcolor=ft.Colors.BLUE_50,
                                border_radius=10
                            ),

                            ft.Divider(height=15),

                            # Información de la factura con mejor diseño
                            ft.Column([
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CALENDAR_TODAY, size=18, color=ft.Colors.BLUE_600),
                                        ft.Text(f.fecha, size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500)
                                    ], spacing=12),
                                    padding=ft.padding.symmetric(vertical=5)
                                ),
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.INVENTORY_2, size=18, color=ft.Colors.GREEN_600),
                                        ft.Text(f"{len(f.detalles)} productos", size=14, color=ft.Colors.GREY_700, weight=ft.FontWeight.W_500)
                                    ], spacing=12),
                                    padding=ft.padding.symmetric(vertical=5)
                                ),
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.ATTACH_MONEY, size=18, color=ft.Colors.PURPLE_600),
                                        ft.Text(f"${f.total:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_700)
                                    ], spacing=12),
                                    padding=ft.padding.symmetric(vertical=5)
                                )
                            ], spacing=5),

                            ft.Divider(height=20),

                            # Espacio para el botón eliminado
                            ft.Container(height=50)
                        ], spacing=10),

                        # Ícono de ojo en la esquina inferior derecha (solo visible cuando seleccionada)
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.REMOVE_RED_EYE,
                                on_click=on_ver_detalles,
                                icon_color=ft.Colors.BLUE_600,
                                bgcolor=ft.Colors.WHITE,
                                width=40,
                                height=40
                            ) if is_selected else ft.Container(),
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.all(10)
                        )
                    ]),
                    padding=20,
                    width=400,
                    height=280,
                    bgcolor=card_bgcolor,
                    border=ft.border.all(4, ft.Colors.BLUE_700) if is_selected else None,
                    border_radius=15
                ),
                elevation=6 if is_selected else 2,
                margin=8,
                shadow_color=ft.Colors.BLUE_400 if is_selected else ft.Colors.BLUE_200
            )
            
            # Envolver el Card en un GestureDetector que soporte eventos de clic
            clickable_card = ft.GestureDetector(
                content=card,
                on_tap=lambda e, fact=f: seleccionar_factura(app_instance, fact),
                on_double_tap=lambda e, fact=f: doble_clic_factura(app_instance, fact)
            )
            
            app.facturas_grid.controls.append(clickable_card)

        app_instance.page.update()

    def init_view():
        """Inicializar la vista"""
        load_facturas()

    # Layout principal siguiendo el patrón de ventas
    content = ft.Column(
        controls=[
            # Header con filtro en la esquina superior derecha
            ft.Container(
                content=ft.Stack([
                    # Título principal
                    ft.Container(
                        content=ft.Text("Facturas", size=32, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.top_left,
                        padding=ft.padding.only(left=20, top=10)
                    ),
                    # Filtro en la esquina superior derecha
                    ft.Container(
                        content=app.facturas_search_field,
                        alignment=ft.alignment.top_right,
                        padding=ft.padding.only(right=20, top=10)
                    )
                ]),
                height=80,
                padding=ft.padding.symmetric(vertical=10)
            ),

            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("📋 Lista de Facturas", size=24, weight=ft.FontWeight.BOLD),
                                ft.Container(
                                    content=ft.Text(f"{len(app.facturas_list)} facturas", size=14, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                    bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                                    border_radius=15
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Container(
                            content=app.facturas_grid,
                            padding=ft.padding.symmetric(vertical=10),
                            height=500
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
        spacing=20,
        scroll=ft.ScrollMode.AUTO
    )

    def seleccionar_factura(app_instance, factura):
        """Lógica de selección: cuando se selecciona una factura, queda seleccionada"""
        # Actualizar la variable en la app
        app_instance.selected_factura = factura

        # Forzar actualización de la vista
        if hasattr(app_instance, 'page'):
            # Re-filtrar para actualizar la visualización
            filtrar_facturas(app_instance)

    def doble_clic_factura(app_instance, factura):
        """Lógica de doble clic: abre el cuadro de diálogo con información de la factura"""
        mostrar_dialogo_factura(app_instance, factura)

    def mostrar_dialogo_factura(app_instance, factura):
        """Lógica de diálogo: mostrar información completa de la factura con opciones de exportar PDF"""
        def cerrar_dialogo(e):
            app_instance.page.dialog.open = False
            app_instance.page.update()

        def exportar_pdf(e):
            try:
                # Cerrar el diálogo primero
                app_instance.page.dialog.open = False
                app_instance.page.update()

                # Generar y guardar PDF
                from fpdf import FPDF
                import os

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Encabezado
                import os
                import sys
                if getattr(sys, 'frozen', False):
                    logo_path = os.path.join(sys._MEIPASS, "VP-logo.png")
                else:
                    logo_path = os.path.join(os.getcwd(), "VP-logo.png")
                if os.path.exists(logo_path):
                    pdf.image(logo_path, x=10, y=8, w=15, h=15)
                    pdf.set_xy(30, 10)
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 10, "VENTA ENTERPRISE", ln=1, align='L')
                pdf.set_font("Arial", size=10)
                pdf.cell(0, 10, f"Factura #{factura.id:04d}", ln=1, align='L')
                pdf.cell(0, 10, f"Fecha: {factura.fecha}", ln=1, align='L')
                pdf.ln(5)

                # Encabezados tabla productos
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(70, 10, "Producto", 1)
                pdf.cell(20, 10, "Cant.", 1, align='C')
                pdf.cell(40, 10, "Precio Bs.", 1, align='R')
                pdf.cell(40, 10, "Precio $", 1, align='R')
                pdf.cell(30, 10, "Total Bs.", 1, align='R')
                pdf.ln()

                pdf.set_font("Arial", size=12)
                total_bs = 0
                total_usd = 0

                for detalle in factura.detalles:
                    nombre = detalle['nombre']
                    cantidad = detalle['cantidad']
                    precio_bs = detalle['precio']
                    # Suponiendo que el precio en dólares está en detalle['precio_usd'], si no, calcularlo
                    precio_usd = detalle.get('precio_usd', round(precio_bs / 24.0, 2))  # Ejemplo tasa de cambio 24
                    total_producto_bs = cantidad * precio_bs
                    total_bs += total_producto_bs
                    total_usd += cantidad * precio_usd

                    pdf.cell(70, 10, nombre, 1)
                    pdf.cell(20, 10, str(cantidad), 1, align='C')
                    pdf.cell(40, 10, f"{precio_bs:.2f}", 1, align='R')
                    pdf.cell(40, 10, f"{precio_usd:.2f}", 1, align='R')
                    pdf.cell(30, 10, f"{total_producto_bs:.2f}", 1, align='R')
                    pdf.ln()

                pdf.ln(10)
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(170, 10, "Subtotal:", 0, align='R')
                pdf.cell(30, 10, f"{total_bs:.2f} Bs.", 0, align='R')
                pdf.ln()
                pdf.cell(170, 10, "Total:", 0, align='R')
                pdf.cell(30, 10, f"{total_bs:.2f} Bs.", 0, align='R')
                pdf.ln()
                pdf.cell(170, 10, "Total (USD):", 0, align='R')
                pdf.cell(30, 10, f"{total_usd:.2f} $", 0, align='R')
                pdf.ln()

                # Crear carpeta si no existe fuera del exe
                carpeta = os.path.join(os.path.expanduser("~"), "VentaEnterprise_facturas_pdf")
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

                filename = f"{carpeta}/factura_{factura.id}.pdf"
                pdf.output(filename)

                # Mostrar mensaje de éxito
                app_instance.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"✅ PDF exportado: {filename}"),
                    bgcolor=ft.Colors.GREEN_600
                )
                app_instance.page.snack_bar.open = True
                app_instance.page.update()

            except Exception as ex:
                app_instance.page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"❌ Error al exportar PDF: {str(ex)}"),
                    bgcolor=ft.Colors.RED_600
                )
                app_instance.page.snack_bar.open = True
                app_instance.page.update()

        # Crear contenido del diálogo con información de la factura
        detalles_productos = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row([
                        ft.Text("Producto", weight=ft.FontWeight.BOLD, width=120),
                        ft.Text("Cant.", weight=ft.FontWeight.BOLD, width=60),
                        ft.Text("Precio", weight=ft.FontWeight.BOLD, width=80),
                        ft.Text("Subtotal", weight=ft.FontWeight.BOLD, width=80),
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.BLUE_400,
                    border_radius=5
                )
            ] + [
                ft.Container(
                    content=ft.Row([
                        ft.Text(detalle['nombre'], width=120),
                        ft.Text(str(detalle['cantidad']), width=60),
                        ft.Text(f"${detalle['precio']:.2f}", width=80),
                        ft.Text(f"${detalle['cantidad'] * detalle['precio']:.2f}", width=80),
                    ]),
                    padding=8,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    bgcolor=ft.Colors.BLUE_GREY_500,
                    border_radius=5
                )
                for detalle in factura.detalles
            ],
            spacing=5,
            height=300,
            scroll=ft.ScrollMode.AUTO
        )

        app_instance.page.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"📄 Detalles de Factura #{factura.id:04d}"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Fecha: {factura.fecha}", size=14),
                    ft.Text(f"Total de productos: {len(factura.detalles)}", size=14),
                    ft.Divider(height=20),
                    ft.Text("DETALLE DE PRODUCTOS:", weight=ft.FontWeight.BOLD),
                    detalles_productos,
                    ft.Divider(height=20),
                    ft.Row([
                        ft.Text("TOTAL:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"${factura.total:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=10),
                width=600,
                height=500
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.ElevatedButton(
                    "Exportar PDF",
                    on_click=exportar_pdf,
                    icon=ft.Icons.PICTURE_AS_PDF,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        app_instance.page.dialog.open = True
        app_instance.page.update()
        # Agregar el diálogo a la página para que se muestre correctamente
        app_instance.page.add(app_instance.page.dialog)

    init_view()
    return content
