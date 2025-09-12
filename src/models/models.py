from ..database import create_connection

class Producto:
    def __init__(self, id=None, nombre='', precio=0.0, stock=0, costo_usd=0.0, porcentaje_ganancia=0.0):
        self.id = id
        self.nombre = nombre
        self.precio = precio  # Precio de venta en VES
        self.stock = stock
        self.costo_usd = costo_usd  # Costo en dólares
        self.porcentaje_ganancia = porcentaje_ganancia  # Porcentaje de ganancia deseado

    @staticmethod
    def get_all():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM productos')
        rows = cursor.fetchall()
        conn.close()
        return [Producto(*row) for row in rows]

    def save(self):
        conn = create_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute('UPDATE productos SET nombre=?, precio=?, stock=? WHERE id=?',
                           (self.nombre, self.precio, self.stock, self.id))
        else:
            cursor.execute('INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)',
                           (self.nombre, self.precio, self.stock))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM productos WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

class Venta:
    def __init__(self, id=None, fecha='', total=0.0, detalles=None):
        self.id = id
        self.fecha = fecha
        self.total = total
        self.detalles = detalles or []

    def save(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ventas (fecha, total) VALUES (?, ?)', (self.fecha, self.total))
        self.id = cursor.lastrowid
        for detalle in self.detalles:
            cursor.execute('INSERT INTO detalle_venta (venta_id, producto_id, cantidad, precio) VALUES (?, ?, ?, ?)',
                           (self.id, detalle['producto_id'], detalle['cantidad'], detalle['precio']))
        conn.commit()
        conn.close()

class Factura:
    def __init__(self, id=None, fecha='', total=0.0, detalles=None):
        self.id = id
        self.fecha = fecha
        self.total = float(total) if total else 0.0
        self.detalles = detalles or []

    @staticmethod
    def get_all():
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM facturas')
        rows = cursor.fetchall()
        conn.close()
        facturas = []
        for row in rows:
            f = Factura(*row)
            f.detalles = Factura.get_detalles(f.id)
            facturas.append(f)
        return facturas

    @staticmethod
    def get_by_id(id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM facturas WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            f = Factura(*row)
            f.detalles = Factura.get_detalles(f.id)
            return f
        return None

    @staticmethod
    def get_detalles(factura_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT df.producto_id, df.cantidad, df.precio, p.nombre
            FROM detalle_factura df
            JOIN productos p ON df.producto_id = p.id
            WHERE df.factura_id = ?
        ''', (factura_id,))
        rows = cursor.fetchall()
        conn.close()
        detalles = []
        for row in rows:
            detalles.append({
                'producto_id': row[0],
                'cantidad': row[1],
                'precio': row[2],
                'nombre': row[3]
            })
        return detalles

    def save(self):
        conn = create_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute('UPDATE facturas SET fecha=?, total=? WHERE id=?',
                           (self.fecha, self.total, self.id))
        else:
            cursor.execute('INSERT INTO facturas (fecha, total) VALUES (?, ?)',
                           (self.fecha, self.total))
            self.id = cursor.lastrowid

        # Guardar detalles (siempre que haya detalles)
        if self.detalles:
            # Primero eliminar detalles existentes si es una actualización
            if self.id:
                cursor.execute('DELETE FROM detalle_factura WHERE factura_id=?', (self.id,))
            # Insertar nuevos detalles
            for detalle in self.detalles:
                cursor.execute('INSERT INTO detalle_factura (factura_id, producto_id, cantidad, precio) VALUES (?, ?, ?, ?)',
                               (self.id, detalle['producto_id'], detalle['cantidad'], detalle['precio']))

        conn.commit()
        conn.close()

    def delete(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM detalle_factura WHERE factura_id=?', (self.id,))
        cursor.execute('DELETE FROM facturas WHERE id=?', (self.id,))
        conn.commit()
        conn.close()
