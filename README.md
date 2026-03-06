# VentaEnterprise

<p align="center">
  <img src="VP-logo.png" alt="VentaEnterprise Logo" width="120" height="120">
</p>

<p align="center">
  <strong>Sistema de Gesti&oacute;n de Ventas Integral</strong>
</p>

<p align="center">
  Aplicaci&oacute;n de escritorio para la gesti&oacute;n completa de ventas, productos, facturas y reportes empresariales.
</p>

---
## Caracter&iacute;sticas Principales

 Caracter&iacute;stica | Descripci&oacute;n |
|:---|:---|
| **Dashboard Ejecutivo** | Panel de control con m&eacute;tricas en tiempo real, gr&aacute;ficos de ventas y estad&iacute;sticas |
| **Gesti&oacute;n de Ventas** | Sistema de ventas con carrito de compras, selecci&oacute;n de productos y facturaci&oacute;n autom&aacute;tica |
| **Control de Inventario** | Gesti&oacute;n completa de productos con precios en USD y VES, control de stock |
| **Sistema de Facturas** | Generaci&oacute;n autom&aacute;tica de facturas con exportaci&oacute;n a PDF |
| **Reportes y An&aacute;lisis** | Reportes detallados con exportaci&oacute;n a Excel, an&aacute;lisis de productos m&aacute;s vendidos |
| **Modo Oscuro/Claro** | Interfaz adaptativa con soporte para tema oscuro y claro |
| **Tasa de Cambio** | Integraci&oacute;n con APIs de tasa de cambio USD/VES con cache local |

---

## Estructura del Proyecto

```
VentaEnterprise/
├── main.py                      # Punto de entrada de la aplicaci&oacute;n
├── VP-logo.png                  # Logo de la aplicaci&oacute;n
├── VP-logo.ico                  # Icono de la aplicaci&oacute;n
├── .gitignore                   # Configuraci&oacute;n de Git
└── src/
    ├── __init__.py
    ├── database.py              # M&oacute;dulo de base de datos SQLite
    ├── controllers/
    │   ├── __init__.py
    │   └── controllers.py       # Controladores de l&oacute;gica de negocio
    ├── models/
    │   ├── __init__.py
    │   └── models.py            # Modelos de datos
    ├── utils/
    │   ├── __init__.py
    │   └── exchange_rate.py     # Servicio de tasas de cambio
    └── views/
        ├── __init__.py
        ├── views.py             # Vista principal y navegaci&oacute;n
        ├── dashboard_view.py    # Dashboard y m&eacute;tricas
        ├── ventas_view.py       # M&oacute;dulo de ventas
        ├── productos_view.py    # Gesti&oacute;n de productos
        ├── factura_view.py     # Gesti&oacute;n de facturas
        └── reportes_view.py     # Reportes y an&aacute;lisis
```

---

## Requisitos Previos

| Requisito | Versi&oacute;n M&iacute;nima | Descripci&oacute;n |
|:---|:---:|:---|
|**Python** | 3.8+ | Int&eacute;rprete de Python |
|**Flet** | 0.21.0 | Framework principal de la interfaz |
|**SQLite** | - | Base de datos (incluida en Python) |
|**Requests** | 2.28+ | Cliente HTTP para APIs |
|**FPDF** | 1.7+ | Generaci&oacute;n de PDFs |
|**OpenPyXL** | 3.0+ | Manipulaci&oacute;n de archivos Excel |
|**Windows** | 10/11 | Sistema operativo (versi&oacute;n actual) |

---

## Instalaci&oacute;n

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Darkangel120/VentaEnterprise.git
cd VentaEnterprise
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install flet>=0.21.0 requests>=2.28.0 fpdf>=1.7.0 openpyxl>=3.0.0
```

### 4. Ejecutar la Aplicaci&oacute;n

```bash
python main.py
```

---

## Configuraci&oacute;n

### Almacenamiento de Datos

La aplicaci&oacute;n crea autom&aacute;ticamente una carpeta oculta en el directorio del usuario:

```
C:\Users\[Usuario]\.ventaenterprise\
```

Esta carpeta contiene:
- `ventaenterprise.db` - Base de datos SQLite
- `exchange_rate_cache.json` - Cache de tasa de cambio
- `dark_mode_pref.json` - Preferencia de modo oscuro

### API de Tasa de Cambio

La aplicaci&oacute;n utiliza las siguientes APIs p&uacute;blicas para obtener la tasa de cambio:

| API | Endpoint | Descripci&oacute;n |
|:---|:---|:---|
| ExchangeDyn | `api.exchangedyn.com` | Tasa oficial BCV |
| DolarAPI | `ve.dolarapi.com` | Promedio del mercado |

El sistema incluye cache de 1 hora para evitar consultas excesivas.

---

## Uso de la Aplicaci&oacute;n

### Inicio de la Aplicaci&oacute;n

Al ejecutar `main.py`, la aplicaci&oacute;n:

1. Crea la carpeta de configuraci&oacute;n oculta
2. Inicializa las tablas de la base de datos
3. Carga la interfaz gr&aacute;fica
4. Muestra el Dashboard principal

### Navegaci&oacute;n

La barra lateral contiene las siguientes opciones:

| Icono | Vista |
:---|:---|
| Dashboard | Panel ejecutivo |
| Ventas | Registro de ventas |
| Productos | Gesti&oacute;n de inventario |
| Facturas | Lista de facturas |
| Reportes | An&aacute;lisis de datos |
| Modo | Alternar tema |

---
## Contribuci&oacute;n

&iexcl;Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva caracter&iacute;stica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## Licencia

Este proyecto est&aacute; bajo la licencia MIT. Ver el archivo `LICENSE` para m&aacute;s detalles.

---

## Autor

| | Informaci&oacute;n |
|:---|:---|
| **Desarrollador** | Darkangel120 |
| **GitHub** | [github.com/Darkangel120](https://github.com/Darkangel120) |

---

## Agradecimientos

| | |
|:---|
| Gracias por usar VentaEnterprise |
| Contribuye al proyecto |
| Dale una estrella en GitHub |

---

<p align="center">
  <strong>VentaEnterprise &copy; 2026</strong>
</p>

<p align="center">
  <img src="VP-logo.png" alt="Logo" width="32" height="32">
</p>

