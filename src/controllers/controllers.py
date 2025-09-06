from ..models.models import Producto, Venta
from ..utils.exchange_rate import ExchangeRateService

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
    def registrar_venta(self, fecha, total, detalles):
        v = Venta(fecha=fecha, total=total, detalles=detalles)
        v.save()
        for detalle in detalles:
            ProductoController().update_stock(detalle['producto_id'], detalle['cantidad'])
