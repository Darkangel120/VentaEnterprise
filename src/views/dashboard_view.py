import flet as ft
from .reportes_view import get_color_with_opacity

def create_professional_metric_card(app, title, value, color, icon, trend, subtitle):
    """Create a professional metric card with icon and trend indicator"""
    # Crear color de fondo con opacidad correcta
    bg_color = get_color_with_opacity(color, 0.2)

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
                ft.Text(title, size=13, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                ft.Text(value, size=28, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(subtitle, size=10, color=ft.Colors.BLUE_GREY_500 if not app.dark_mode else ft.Colors.BLUE_GREY_500),
            ],
            spacing=6
        ),
        width=300,
        height=150,
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
        border_radius=20,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=12,
            color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
        )
    )

def create_enhanced_bar(self, day, amount, height, color):
    """Create an enhanced bar with tooltip for value display"""
    # Formatear el valor con separadores de miles y 2 decimales
    formatted_amount = f"${amount:,.2f}"

    return ft.Container(
        content=ft.Column(
            controls=[
                # The bar itself with tooltip
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                height=height,
                                width=50,  # Aumentado para barras más anchas
                                bgcolor=color,
                                border_radius=ft.border_radius.all(8),
                                shadow=ft.BoxShadow(
                                    spread_radius=2,
                                    blur_radius=8,
                                    color=ft.Colors.BLUE_200
                                ),
                                tooltip=formatted_amount  # Tooltip con el valor formateado
                            ),
                            # Base of the bar
                            ft.Container(
                                height=6,
                                width=60,  # Aumentado para coincidir con la barra
                                bgcolor=ft.Colors.BLUE_300,
                                border_radius=ft.border_radius.all(10)
                            )
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.END
                    ),
                    height=height + 6,
                    alignment=ft.alignment.bottom_center
                ),
                # Day label
                ft.Container(
                    content=ft.Text(day, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800 if not self.dark_mode else ft.Colors.BLUE_GREY_300),
                    height=28,
                    alignment=ft.alignment.center
                )
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.END
        ),
        height=height + 38,  # Ajustado ya que quitamos el texto encima
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

import datetime

def create_sales_chart(app, view_type="monthly"):
    """Create an enhanced sales chart with real data from database"""
    today = datetime.date.today()
    year_start = datetime.date(today.year, 1, 1)
    days_passed = (today - year_start).days + 1  # inclusive

    if view_type == "weekly":
        # Obtener datos del año completo
        datos_ventas = app.venta_controller.get_datos_grafico_ventas(dias=days_passed)
        # Agrupar por semanas (semana 1 a semana N)
        ventas_agrupadas = []
        semanas_totales = (days_passed + 6) // 7  # número de semanas completas o parciales
        for i in range(semanas_totales):
            semana_sum = sum(datos_ventas[i*7:(i+1)*7])
            ventas_agrupadas.append(semana_sum)
        # Etiquetas de semanas
        period_labels = [f"Sem {i+1}" for i in range(semanas_totales)]
        period_name = "semanal"
        total_label = "Total Semana"
        comparison_text = "vs semana anterior"
        metric_label = "Mejor Semana"
    else:  # monthly
        # Obtener datos del año completo
        datos_ventas = app.venta_controller.get_datos_grafico_ventas(dias=days_passed)
        ventas_agrupadas = []
        # Agrupar por meses
        month_days = [31, 29 if (today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month_labels = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        start_idx = 0
        for md in month_days:
            if start_idx >= len(datos_ventas):
                ventas_agrupadas.append(0)
            else:
                ventas_agrupadas.append(sum(datos_ventas[start_idx:start_idx+md]))
            start_idx += md
        # Ajustar etiquetas para meses con datos
        period_labels = month_labels[:len(ventas_agrupadas)]
        period_name = "mensual"
        total_label = "Total Mes"
        comparison_text = "vs mes anterior"
        metric_label = "Mejor Mes"

    # Calcular estadísticas
    total_periodo = sum(ventas_agrupadas) if ventas_agrupadas else 0
    promedio_periodo = total_periodo / len(ventas_agrupadas) if ventas_agrupadas else 0
    max_venta = max(ventas_agrupadas) if ventas_agrupadas else 0
    mejor_periodo_idx = ventas_agrupadas.index(max_venta) if ventas_agrupadas and max_venta > 0 else 0
    mejor_periodo = period_labels[mejor_periodo_idx] if ventas_agrupadas else "N/A"

    # Calcular promedio diario basado en los datos diarios (para métricas adicionales)
    promedio_diario = sum(datos_ventas) / len(datos_ventas) if datos_ventas else 0

    # Calcular altura máxima para las barras (normalizar)
    max_altura = 250
    max_valor = max(ventas_agrupadas) if ventas_agrupadas else 1

    # Ajustar factor de escala para evitar barras demasiado altas
    escala = 1.0
    if max_valor > 10000000:
        escala = 0.5
    elif max_valor > 5000000:
        escala = 0.7
    elif max_valor > 1000000:
        escala = 0.9

    # Crear barras del gráfico
    barras = []
    colores = [ft.Colors.BLUE_500, ft.Colors.BLUE_600, ft.Colors.BLUE_500,
              ft.Colors.BLUE_700, ft.Colors.BLUE_600, ft.Colors.BLUE_700, ft.Colors.BLUE_500,
              ft.Colors.BLUE_400, ft.Colors.BLUE_500, ft.Colors.BLUE_600, ft.Colors.BLUE_700, ft.Colors.BLUE_500]

    for i, (periodo, valor) in enumerate(zip(period_labels[:len(ventas_agrupadas)], ventas_agrupadas)):
        altura = int((valor / max_valor) * max_altura * escala) if max_valor > 0 else 0
        barras.append(create_enhanced_bar(app, periodo, valor, altura, colores[i % len(colores)]))

    return ft.Container(
        content=ft.Column(
            controls=[
                # Header with title and summary
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("📈 Análisis de Ventas Detallado", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Tendencia {period_name} con métricas clave", size=12, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                            ],
                            spacing=2,
                            alignment=ft.MainAxisAlignment.START,
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(f"${total_periodo:.2f}", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN),
                                    ft.Text(total_label, size=10, color=ft.Colors.BLUE_GREY_500),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.END
                            ),
                            padding=ft.padding.symmetric(horizontal=15, vertical=8),
                            bgcolor=ft.Colors.GREEN_50 if not app.dark_mode else ft.Colors.GREEN_900,
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
                                    spacing=15 if view_type == "monthly" else 20,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                                height=280,
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
                                                    ft.Text(comparison_text, size=10, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                                                ],
                                                spacing=5,
                                                alignment=ft.MainAxisAlignment.START
                                                ),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                            bgcolor=ft.Colors.GREEN_50 if not app.dark_mode else ft.Colors.GREEN_900,
                                            border_radius=15
                                        ),
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.STAR, size=16, color=ft.Colors.ORANGE),
                                                    ft.Text(f"{mejor_periodo} pico", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE),
                                                    ft.Text(f"${max_venta:.2f}", size=10, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                                                ],
                                                spacing=5,
                                                alignment=ft.MainAxisAlignment.START
                                            ),
                                            padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                            bgcolor=ft.Colors.ORANGE_50 if not app.dark_mode else ft.Colors.ORANGE_900,
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
                                        create_mini_metric(app, "Promedio Diario", f"${promedio_diario:.2f}", ft.Colors.BLUE),
                                        create_mini_metric(app, metric_label, mejor_periodo, ft.Colors.GREEN),
                                        create_mini_metric(app, "Transacciones", str(sum(1 for v in datos_ventas if v > 0)), ft.Colors.PURPLE),
                                    ],
                                    spacing=15,
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                                ),
                                padding=ft.padding.symmetric(vertical=10)
                            )
                        ],
                        spacing=15
                    ),
                    height=350,
                    alignment=ft.alignment.center
                )
            ],
            spacing=15
        ),
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
        border_radius=15,
        padding=ft.padding.all(20)
    )

def create_top_product_item_pro(app, name, price, sales, medal_color):
    """Create a top product item with medal icon"""
    # Crear color de fondo con opacidad correcta
    bg_color = get_color_with_opacity(medal_color, 0.2)

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
                    content=ft.Text(sales, size=12, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                    padding=ft.padding.symmetric(horizontal=10, vertical=5),
                    bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
                    border_radius=15
                )
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=ft.padding.symmetric(horizontal=15, vertical=12),
        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_800,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=6,
            color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
        )
    )

def create_top_products_list(app):
    """Create a list of top products from database"""
    try:
        # Obtener productos más vendidos de la base de datos
        top_products = app.venta_controller.get_productos_mas_vendidos(limit=4)

        if not top_products:
            return [
                ft.Text("No hay datos de ventas disponibles", size=14, color=ft.Colors.GREY)
            ]

        product_items = []
        medal_colors = [ft.Colors.YELLOW, ft.Colors.GREY, ft.Colors.ORANGE, ft.Colors.BLUE_GREY]

        for i, product in enumerate(top_products):
            medal_color = medal_colors[i] if i < len(medal_colors) else ft.Colors.BLUE_GREY
            item = create_top_product_item_pro(app, product['nombre'], f"${product['precio']:.2f}", f"{product['ventas']} ventas", medal_color)
            product_items.append(item)

        return product_items

    except Exception as e:
        print(f"Error al obtener productos destacados: {e}")
        return [
            ft.Text("Error al cargar productos destacados", size=14, color=ft.Colors.RED)
        ]

def create_quick_stat(app, label, value, color):
    """Create a quick statistic item"""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(label, size=12, color=ft.Colors.BLUE_GREY_600 if not app.dark_mode else ft.Colors.BLUE_GREY_400),
                ft.Text(value, size=14, weight=ft.FontWeight.BOLD, color=color)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
        border_radius=10
    )

def create_quick_stats_list(app):
    """Create a list of quick statistics"""
    try:
        # Get some basic statistics
        ventas_dia = app.venta_controller.get_ventas_del_dia()
        productos_vendidos = app.venta_controller.get_productos_vendidos_hoy()
        clientes_atendidos = app.venta_controller.get_clientes_atendidos_hoy()

        return [
            create_quick_stat(app, "Ventas Hoy", f"${ventas_dia:.2f}", ft.Colors.GREEN),
            create_quick_stat(app, "Productos Vendidos", str(productos_vendidos), ft.Colors.BLUE),
            create_quick_stat(app, "Transacciones Hoy", str(clientes_atendidos), ft.Colors.ORANGE),
        ]
    except Exception as e:
        print(f"Error al obtener estadísticas rápidas: {e}")
        return [
            create_quick_stat(app, "Error", "No disponible", ft.Colors.RED),
        ]

def create_status_badge(app, status, color):
    """Create a status badge"""
    return ft.Container(
        content=ft.Text(status, size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        bgcolor=color,
        border_radius=12
    )

def create_recent_activity_rows(app):
    """Create recent activity rows from database"""
    try:
        # Obtener ventas recientes de la base de datos
        ventas_recientes = app.venta_controller.get_ventas_recientes(limit=4)

        if not ventas_recientes:
            return [
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("--:--", size=13)),
                    ft.DataCell(ft.Text("Sin ventas recientes", size=13)),
                    ft.DataCell(ft.Text("0 items", size=13)),
                    ft.DataCell(ft.Text("$0.00", color=ft.Colors.GREY, weight=ft.FontWeight.BOLD, size=13)),
                    ft.DataCell(create_status_badge(app, "Sin datos", ft.Colors.GREY)),
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
                ft.DataCell(create_status_badge(app, estado, estado_color)),
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
                ft.DataCell(create_status_badge(app, "Error", ft.Colors.RED)),
            ])
        ]

def build_dashboard(app):
    """Build the main dashboard view"""
    # Obtener datos reales de la base de datos
    ventas_dia = app.venta_controller.get_ventas_del_dia()
    productos_vendidos = app.venta_controller.get_productos_vendidos_hoy()
    clientes_atendidos = app.venta_controller.get_clientes_atendidos_hoy()
    valor_inventario = app.venta_controller.get_valor_inventario()

    # Contenedor para el gráfico mensual
    chart_container = ft.Container(
        content=create_sales_chart(app, "monthly"),
        height=400,
        alignment=ft.alignment.center
    )

    return ft.Container(
        expand=True,
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
                        colors=[ft.Colors.BLUE_700, ft.Colors.PURPLE_700] if not app.dark_mode else [ft.Colors.BLUE_900, ft.Colors.PURPLE_900]
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
                                on_click=lambda e: app.change_view("ventas")
                            ),
                            ft.ElevatedButton(
                                "Agregar Producto",
                                icon=ft.Icons.ADD_BOX,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.BLUE_600,
                                    color=ft.Colors.WHITE,
                                    elevation=3
                                ),
                                on_click=lambda e: app.change_view("productos")
                            ),
                            ft.ElevatedButton(
                                "Ver Reportes",
                                icon=ft.Icons.ANALYTICS,
                                style=ft.ButtonStyle(
                                    bgcolor=ft.Colors.ORANGE_600,
                                    color=ft.Colors.WHITE,
                                    elevation=3
                                ),
                                on_click=lambda e: app.change_view("reportes")
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
                            create_professional_metric_card(
                                app, "Ventas del Día", f"${ventas_dia:.2f}", ft.Colors.GREEN,
                                ft.Icons.TRENDING_UP, "+18%", "vs ayer"
                            ),
                            create_professional_metric_card(
                                app, "Productos Vendidos", str(productos_vendidos), ft.Colors.BLUE,
                                ft.Icons.SHOPPING_BAG, "+12%", "esta semana"
                            ),
                            create_professional_metric_card(
                                app, "Transacciones del Día", str(clientes_atendidos), ft.Colors.ORANGE,
                                ft.Icons.RECEIPT, "+25%", "este mes"
                            ),
                            create_professional_metric_card(
                                app, "Valor en Inventario", f"${valor_inventario:.2f}", ft.Colors.PURPLE,
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
                                        content=ft.Text("Año actual", size=12, color=ft.Colors.BLUE_GREY_600),
                                        bgcolor=ft.Colors.BLUE_GREY_100 if not app.dark_mode else ft.Colors.BLUE_GREY_800,
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
                                                chart_container
                                            ],
                                            spacing=15
                                        ),
                                        expand=True,
                                        padding=25,
                                        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                                        border_radius=20,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=12,
                                            color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
                                        )
                                    ),

                                    # Top Products & Quick Stats
                                    ft.Container(
                                        content=ft.Column(
                                            controls=[
                                                ft.Text("🏆 Productos Destacados", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Column(
                                                    controls=create_top_products_list(app),
                                                    spacing=12
                                                ),

                                                ft.Divider(height=20),

                                                ft.Text("📈 Estadísticas Rápidas", size=16, weight=ft.FontWeight.BOLD),
                                                ft.Column(
                                                    controls=create_quick_stats_list(app),
                                                    spacing=8
                                                )
                                            ],
                                            spacing=20
                                        ),
                                        width=350,
                                        padding=25,
                                        bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                                        border_radius=20,
                                        shadow=ft.BoxShadow(
                                            spread_radius=1,
                                            blur_radius=12,
                                            color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
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
                                                on_click=lambda e: app.change_view("facturas")
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
                                    rows=create_recent_activity_rows(app),
                                    width=1000,
                                    height=300,
                                    border_radius=15,
                                    heading_row_height=50,
                                    data_row_min_height=50,
                                    heading_row_color=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_800
                                ),
                                padding=25,
                                bgcolor=ft.Colors.WHITE if not app.dark_mode else ft.Colors.BLUE_GREY_900,
                                border_radius=20,
                                shadow=ft.BoxShadow(
                                    spread_radius=1,
                                    blur_radius=12,
                                    color=ft.Colors.BLACK12 if not app.dark_mode else ft.Colors.BLACK26
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
        bgcolor=ft.Colors.BLUE_GREY_50 if not app.dark_mode else ft.Colors.BLUE_GREY_900
    )