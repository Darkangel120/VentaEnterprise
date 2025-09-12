from ..models.models import Producto, Venta, Factura
from ..database import create_connection
from ..utils.exchange_rate import ExchangeRateService
from datetime import datetime, timedelta

class ProductoController:
    def __init__(self):
        self.exchange_service = ExchangeRateService()

    def get_all(self):
        return Producto.get_all()

    def add_producto(self, nombre, precio, stock, costo_usd=0.0, porcentaje_ganancia=0.0):
        p = Producto(nombre=nombre, precio=precio, stock=stock, costo_usd=costo_usd, porcentaje_ganancia=porcentaje_ganancia)
        p.save()

    def update_producto(self, id, nombre, precio, stock, costo_usd=0.0, porcentaje_ganancia=0.0):
        p = Producto(id=id, nombre=nombre, precio=precio, stock=stock, costo_usd=costo_usd, porcentaje_ganancia=porcentaje_ganancia)
        p.save()

    def update_producto_stock(self, producto_id, nuevo_stock):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET stock = ? WHERE id = ?', (nuevo_stock, producto_id))
        conn.commit()
        conn.close()

    def delete_producto(self, id):
        p = Producto(id=id)
        p.delete()

    def update_stock(self, id, cantidad):
        p = Producto(id=id)
        p.stock -= cantidad
        if p.stock < 0:
            p.stock = 0
        p.save()

    def calcular_precio_venta(self, costo_usd, porcentaje_ganancia):
        """Calcula el precio de venta en VES basado en costo USD y porcentaje de ganancia"""
        if costo_usd <= 0 or porcentaje_ganancia < 0:
            return 0.0

        # Calcular precio de venta en USD
        precio_venta_usd = costo_usd * (1 + porcentaje_ganancia / 100)

        # Convertir a VES usando tasa actual
        rate = self.exchange_service.get_dollar_rate()
        if rate:
            return precio_venta_usd * rate
        else:
            return 0.0

    def get_exchange_rate(self):
        """Obtiene la tasa de cambio actual"""
        return self.exchange_service.get_dollar_rate()

    def calcular_ganancias(self, producto, cantidad=1):
        """Calcula las ganancias para un producto"""
        if not producto.costo_usd or not producto.porcentaje_ganancia:
            return None

        return self.exchange_service.calculate_profit(
            producto.costo_usd,
            producto.costo_usd * (1 + producto.porcentaje_ganancia / 100),
            cantidad
        )

class VentaController:
    def __init__(self):
        pass

    def registrar_venta(self, fecha, total, detalles):
        v = Venta(fecha=fecha, total=total, detalles=detalles)
        v.save()
        # Nota: El stock ya se actualiza en finalizar_venta, no es necesario hacerlo aquí

    def get_ventas_del_dia(self):
        """Obtiene el total de ventas del día actual"""
        conn = create_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT SUM(total) FROM ventas WHERE DATE(fecha) = ?', (today,))
        result = cursor.fetchone()[0] or 0.0
        conn.close()
        return result

    def get_productos_vendidos_hoy(self):
        """Obtiene la cantidad total de productos vendidos hoy"""
        conn = create_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT SUM(dv.cantidad)
            FROM detalle_venta dv
            JOIN ventas v ON dv.venta_id = v.id
            WHERE DATE(v.fecha) = ?
        ''', (today,))
        result = cursor.fetchone()[0] or 0
        conn.close()
        return result

    def get_clientes_atendidos_hoy(self):
        """Obtiene el número de clientes atendidos hoy (número de ventas)"""
        conn = create_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM ventas WHERE DATE(fecha) = ?', (today,))
        result = cursor.fetchone()[0] or 0
        conn.close()
        return result

    def get_valor_inventario(self):
        """Calcula el valor total del inventario"""
        productos = ProductoController().get_all()
        return sum(p.precio * p.stock for p in productos)

    def get_productos_destacados(self, limit=3):
        """Obtiene los productos más vendidos"""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.cantidad * dv.precio) as ingresos
            FROM productos p
            JOIN detalle_venta dv ON p.id = dv.producto_id
            GROUP BY p.id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()

        productos_destacados = []
        for row in results:
            productos_destacados.append({
                'nombre': row[0],
                'ventas': row[1],
                'ingresos': row[2]
            })
        return productos_destacados

    def get_productos_mas_vendidos(self, limit=4):
        """Obtiene los productos más vendidos con información completa"""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.cantidad * dv.precio) as ingresos, p.precio
            FROM productos p
            JOIN detalle_venta dv ON p.id = dv.producto_id
            GROUP BY p.id, p.nombre, p.precio
            ORDER BY total_vendido DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()

        productos_mas_vendidos = []
        for row in results:
            productos_mas_vendidos.append({
                'nombre': row[0],
                'ventas': row[1],
                'ingresos': row[2],
                'precio': row[3]
            })
        return productos_mas_vendidos

    def get_actividad_reciente(self, limit=5):
        """Obtiene las ventas más recientes"""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.fecha, v.total,
                   GROUP_CONCAT(p.nombre || ' (' || dv.cantidad || ')') as productos
            FROM ventas v
            JOIN detalle_venta dv ON v.id = dv.venta_id
            JOIN productos p ON dv.producto_id = p.id
            GROUP BY v.id, v.fecha, v.total
            ORDER BY v.fecha DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()

        actividad = []
        for row in results:
            actividad.append({
                'fecha': row[0],
                'total': row[1],
                'productos': row[2] or 'Sin productos'
            })
        return actividad

    def get_ventas_recientes(self, limit=4):
        """Obtiene las ventas más recientes con detalles para la tabla de actividad"""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.id, v.fecha, v.total,
                   SUM(dv.cantidad) as cantidad_total,
                   COUNT(DISTINCT dv.producto_id) as productos_distintos
            FROM ventas v
            JOIN detalle_venta dv ON v.id = dv.venta_id
            GROUP BY v.id, v.fecha, v.total
            ORDER BY v.fecha DESC
            LIMIT ?
        ''', (limit,))
        results = cursor.fetchall()
        conn.close()

        ventas_recientes = []
        for row in results:
            # Obtener detalles de productos para esta venta
            detalles = self.get_detalles_venta(row[0])

            venta = {
                'id': row[0],
                'fecha': row[1],
                'total': row[2],
                'cliente': f'Venta #{row[0]}',  # Usar ID de venta como cliente temporal
                'detalles': detalles
            }
            ventas_recientes.append(venta)

        return ventas_recientes

    def get_detalles_venta(self, venta_id):
        """Obtiene los detalles de una venta específica"""
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT dv.producto_id, dv.cantidad, dv.precio, p.nombre
            FROM detalle_venta dv
            JOIN productos p ON dv.producto_id = p.id
            WHERE dv.venta_id = ?
        ''', (venta_id,))
        results = cursor.fetchall()
        conn.close()

        detalles = []
        for row in results:
            detalles.append({
                'producto_id': row[0],
                'cantidad': row[1],
                'precio': row[2],
                'nombre': row[3]
            })

        return detalles

    def get_datos_grafico_ventas(self, dias=7):
        """Obtiene datos para el gráfico de ventas de los últimos N días"""
        conn = create_connection()
        cursor = conn.cursor()
        fecha_inicio = (datetime.now() - timedelta(days=dias-1)).strftime('%Y-%m-%d')

        cursor.execute('''
            SELECT DATE(fecha) as fecha, SUM(total) as total
            FROM ventas
            WHERE DATE(fecha) >= ?
            GROUP BY DATE(fecha)
            ORDER BY DATE(fecha)
        ''', (fecha_inicio,))
        results = cursor.fetchall()
        conn.close()

        # Crear diccionario con fechas y montos
        datos = {}
        for i in range(dias):
            fecha = (datetime.now() - timedelta(days=dias-1-i)).strftime('%Y-%m-%d')
            datos[fecha] = 0.0

        for row in results:
            datos[row[0]] = row[1]

        return list(datos.values())

    def get_estadisticas_reportes(self):
        """Obtiene estadísticas para la vista de reportes"""
        conn = create_connection()
        cursor = conn.cursor()

        # Productos más vendidos
        cursor.execute('''
            SELECT p.nombre, SUM(dv.cantidad) as cantidad, SUM(dv.cantidad * dv.precio) as ingresos
            FROM productos p
            JOIN detalle_venta dv ON p.id = dv.producto_id
            GROUP BY p.id, p.nombre
            ORDER BY cantidad DESC
            LIMIT 5
        ''')
        productos_mas_vendidos = cursor.fetchall()

        # Clientes nuevos (estimación basada en ventas)
        cursor.execute('SELECT COUNT(*) FROM ventas')
        total_ventas = cursor.fetchone()[0] or 0

        # Promedio por venta
        cursor.execute('SELECT AVG(total) FROM ventas')
        promedio_venta = cursor.fetchone()[0] or 0.0

        conn.close()

        return {
            'productos_mas_vendidos': productos_mas_vendidos,
            'total_ventas': total_ventas,
            'promedio_venta': promedio_venta
        }

class FacturaController:
    def __init__(self):
        pass

    def get_all(self):
        return Factura.get_all()

    def get_by_id(self, id):
        return Factura.get_by_id(id)

    def crear_factura(self, fecha, total, detalles):
        f = Factura(fecha=fecha, total=total, detalles=detalles)
        f.save()
        return f

    def actualizar_factura(self, id, fecha, total):
        f = Factura.get_by_id(id)
        if f:
            f.fecha = fecha
            f.total = total
            f.save()

    def eliminar_factura(self, id):
        f = Factura.get_by_id(id)
        if f:
            f.delete()
