import flet as ft

def get_color_with_opacity(color, opacity):
    """Convertir un color de Flet a uno con opacidad"""
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
        return ft.Colors.BLUE_GREY_200

def create_metric_card(app, title, value, color, icon):
    # Crear color de fondo con opacidad correcta
    bg_color = get_color_with_opacity(color, 0.2)

    # Colores adaptativos para texto
    text_color = ft.Colors.BLACK if not app.dark_mode else ft.Colors.WHITE
    icon_color = ft.Colors.BLACK if not app.dark_mode else ft.Colors.WHITE

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icon, size=40, color=icon_color),
                    width=60,
                    height=60,
                    alignment=ft.alignment.center,
                    bgcolor=bg_color,
                    border_radius=15
                ),
                ft.Text(title, size=14, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color=text_color),
                ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=text_color, text_align=ft.TextAlign.CENTER),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        width=320,
        height=160,
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=12,
            color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
        )
    )

def build_reportes_view(app):
    # Obtener datos reales de la base de datos
    estadisticas = app.venta_controller.get_estadisticas_reportes()

    # Crear métricas dinámicas mejoradas
    metricas = []

    if estadisticas['productos_mas_vendidos']:
        producto_top = estadisticas['productos_mas_vendidos'][0]
        metricas.append(create_metric_card(
            app,
            "Producto Más Vendido",
            producto_top[0],  # nombre del producto
            ft.Colors.GREEN,
            ft.Icons.STAR
        ))
    else:
        metricas.append(create_metric_card(
            app,
            "Producto Más Vendido",
            "Sin datos",
            ft.Colors.GREY,
            ft.Icons.STAR
        ))

    metricas.append(create_metric_card(
        app,
        "Total de Ventas",
        str(estadisticas['total_ventas']),
        ft.Colors.BLUE,
        ft.Icons.SHOPPING_CART
    ))

    metricas.append(create_metric_card(
        app,
        "Promedio por Venta",
        f"${estadisticas['promedio_venta']:.2f}",
        ft.Colors.PURPLE,
        ft.Icons.ATTACH_MONEY
    ))

    # Calcular totales para porcentajes
    total_ventas = sum(cantidad for _, cantidad, _ in estadisticas['productos_mas_vendidos']) if estadisticas['productos_mas_vendidos'] else 0
    total_ingresos = sum(ingresos for _, _, ingresos in estadisticas['productos_mas_vendidos']) if estadisticas['productos_mas_vendidos'] else 0

    # Crear filas de la tabla de análisis mejorada
    table_rows = []
    if estadisticas['productos_mas_vendidos']:
        for producto in estadisticas['productos_mas_vendidos']:
            nombre, cantidad, ingresos = producto
            # Obtener stock restante del producto
            producto_info = next((p for p in app.productos if p.nombre == nombre), None)
            stock_restante = producto_info.stock if producto_info else 0
            precio_promedio = ingresos / cantidad if cantidad > 0 else 0

            # Calcular porcentajes
            porcentaje_ventas = (cantidad / total_ventas * 100) if total_ventas > 0 else 0
            porcentaje_ingresos = (ingresos / total_ingresos * 100) if total_ingresos > 0 else 0

            # Determinar tendencia (simulada - en producción usar datos históricos)
            tendencia = "↗️" if porcentaje_ventas > 15 else "➡️" if porcentaje_ventas > 5 else "↘️"
            tendencia_color = ft.Colors.GREEN if porcentaje_ventas > 15 else ft.Colors.ORANGE if porcentaje_ventas > 5 else ft.Colors.RED

            table_rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                    ft.Text(nombre, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)
                ], spacing=8)),
                ft.DataCell(ft.Column([
                    ft.Text(str(cantidad), weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                    ft.Text(f"{porcentaje_ventas:.1f}%", size=10, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)),
                ft.DataCell(ft.Column([
                    ft.Text(f"${ingresos:.2f}", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                    ft.Text(f"{porcentaje_ingresos:.1f}%", size=10, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)
                ], spacing=2, alignment=ft.MainAxisAlignment.CENTER)),
                ft.DataCell(ft.Text(f"${precio_promedio:.2f}", size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                ft.DataCell(ft.Container(
                    content=ft.Text(tendencia, size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                    alignment=ft.alignment.center,
                    bgcolor=get_color_with_opacity(tendencia_color, 0.2),
                    padding=ft.padding.all(8),
                    border_radius=8
                )),
                ft.DataCell(ft.Container(
                    content=ft.Text(str(stock_restante), size=14, color=ft.Colors.BLACK if not app.dark_mode else ft.Colors.WHITE),
                    alignment=ft.alignment.center,
                    bgcolor=ft.Colors.RED_50 if stock_restante < 10 else ft.Colors.GREEN_50 if stock_restante > 50 else ft.Colors.ORANGE_50,
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=12
                )),
            ]))
    else:
        table_rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text("No hay datos de ventas disponibles", col=6, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
            ft.DataCell(ft.Text("")),
        ]))

    # Agregar fila de resumen
    if estadisticas['productos_mas_vendidos']:
        table_rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Row([
                ft.Icon(ft.Icons.ANALYTICS, size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                ft.Text("TOTAL", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)
            ], spacing=8)),
            ft.DataCell(ft.Text(str(total_ventas), weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
            ft.DataCell(ft.Text(f"${total_ingresos:.2f}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
            ft.DataCell(ft.Text("—", size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
            ft.DataCell(ft.Text("📊", size=16, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
            ft.DataCell(ft.Text("—", size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
        ]))

    # Controles de filtro y ordenamiento
    filter_controls = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("🔍 Filtros:", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                ft.ElevatedButton(
                    "Ordenar por Ventas",
                    icon=ft.Icons.SORT,
                    on_click=lambda e: app.sort_table_by("ventas"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)
                ),
                ft.ElevatedButton(
                    "Ordenar por Ingresos",
                    icon=ft.Icons.SORT,
                    on_click=lambda e: app.sort_table_by("ingresos"),
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)
                ),
                ft.ElevatedButton(
                    "Exportar CSV",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=app.export_reportes_csv,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE)
                ),
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=ft.padding.symmetric(vertical=10)
    )

    return ft.Column(
        controls=[
            # Header mejorado
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("📊 Reportes Detallados", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                                ft.Text("Análisis avanzado de ventas con métricas detalladas", size=16, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                            ],
                            spacing=5,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(f"{len(estadisticas['productos_mas_vendidos']) if estadisticas['productos_mas_vendidos'] else 0}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE),
                                    ft.Text("Productos Analizados", size=12, color=ft.Colors.BLUE_GREY_500 if not app.dark_mode else ft.Colors.BLUE_GREY_300),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.END
                            ),
                            padding=ft.padding.symmetric(horizontal=20, vertical=15),
                            bgcolor=ft.Colors.BLUE_50 if not app.dark_mode else ft.Colors.BLUE_900,
                            border_radius=15
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.symmetric(vertical=20)
            ),

            ft.Divider(height=20),

            # Métricas Cards
            ft.Container(
                content=ft.Row(
                    controls=metricas,
                    spacing=20,
                    wrap=True
                ),
                padding=ft.padding.symmetric(vertical=10)
            ),

            ft.Divider(height=30),

            # Sección de tabla mejorada
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("📈 Análisis de Ventas Detallado", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK),
                                ft.Container(
                                    content=ft.Text("Datos en tiempo real", size=12, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                                    bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                    border_radius=15
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),

                        # Controles de filtro
                        filter_controls,

                        # Tabla mejorada
                        ft.Container(
                            content=ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Producto", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                    ft.DataColumn(ft.Text("Ventas", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                    ft.DataColumn(ft.Text("Ingresos", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                    ft.DataColumn(ft.Text("Precio Promedio", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                    ft.DataColumn(ft.Text("Tendencia", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                    ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.WHITE if app.dark_mode else ft.Colors.BLACK)),
                                ],
                                rows=table_rows,
                                expand=True,
                                height=600,
                                border_radius=15,
                                heading_row_height=60,
                                data_row_min_height=55,
                                data_row_max_height=70,
                                heading_row_color=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                                data_row_color={
                                    "hovered": ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800
                                }
                            ),
                            padding=25,
                            bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                            border_radius=20,
                            shadow=ft.BoxShadow(
                                spread_radius=2,
                                blur_radius=15,
                                color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
                            )
                        ),

                        # Leyenda
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Text("↗️", size=14, color=ft.Colors.GREEN_50),
                                            ft.Text("Alta demanda", size=12, color=ft.Colors.GREEN_50)
                                        ], spacing=5),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        bgcolor=ft.Colors.GREEN_500,
                                        border_radius=10
                                    ),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Text("➡️", size=14, color=ft.Colors.ORANGE_50),
                                            ft.Text("Demanda media", size=12, color=ft.Colors.ORANGE_50)
                                        ], spacing=5),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        bgcolor=ft.Colors.ORANGE_500,
                                        border_radius=10
                                    ),
                                    ft.Container(
                                        content=ft.Row([
                                            ft.Text("↘️", size=14, color=ft.Colors.RED_50),
                                            ft.Text("Baja demanda", size=12, color=ft.Colors.RED_50)
                                        ], spacing=5),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                        bgcolor=ft.Colors.RED_500,
                                        border_radius=10
                                    ),
                                ],
                                spacing=15,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            padding=ft.padding.symmetric(vertical=15)
                        )
                    ],
                    spacing=20
                ),
                padding=ft.padding.symmetric(horizontal=20, vertical=10)
            )
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO
    )


