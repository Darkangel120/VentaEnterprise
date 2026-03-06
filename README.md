<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

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

| &Iacute;cono | Caracter&iacute;stica | Descripci&oacute;n |
|:---:|:---|:---|
| <i class="fas fa-tachometer-alt"></i> | **Dashboard Ejecutivo** | Panel de control con m&eacute;tricas en tiempo real, gr&aacute;ficos de ventas y estad&iacute;sticas |
| <i class="fas fa-shopping-cart"></i> | **Gesti&oacute;n de Ventas** | Sistema de ventas con carrito de compras, selecci&oacute;n de productos y facturaci&oacute;n autom&aacute;tica |
| <i class="fas fa-boxes"></i> | **Control de Inventario** | Gesti&oacute;n completa de productos con precios en USD y VES, control de stock |
| <i class="fas fa-file-invoice"></i> | **Sistema de Facturas** | Generaci&oacute;n autom&aacute;tica de facturas con exportaci&oacute;n a PDF |
| <i class="fas fa-chart-line"></i> | **Reportes y An&aacute;lisis** | Reportes detallados con exportaci&oacute;n a Excel, an&aacute;lisis de productos m&aacute;s vendidos |
| <i class="fas fa-moon"></i> / <i class="fas fa-sun"></i> | **Modo Oscuro/Claro** | Interfaz adaptativa con soporte para tema oscuro y claro |
| <i class="fas fa-exchange-alt"></i> | **Tasa de Cambio** | Integraci&oacute;n con APIs de tasa de cambio USD/VES con cache local |

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
| <i class="fab fa-python"></i> **Python** | 3.8+ | Int&eacute;rprete de Python |
| <i class="fab fa-flutter"></i> **Flet** | 0.21.0 | Framework principal de la interfaz |
| <i class="fas fa-database"></i> **SQLite** | - | Base de datos (incluida en Python) |
| <i class="fas fa-paper-plane"></i> **Requests** | 2.28+ | Cliente HTTP para APIs |
| <i class="fas fa-file-pdf"></i> **FPDF** | 1.7+ | Generaci&oacute;n de PDFs |
| <i class="fas fa-file-excel"></i> **OpenPyXL** | 3.0+ | Manipulaci&oacute;n de archivos Excel |
| <i class="fab fa-windows"></i> **Windows** | 10/11 | Sistema operativo (versi&oacute;n actual) |

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
- <i class="fas fa-database"></i> `ventaenterprise.db` - Base de datos SQLite
- <i class="fas fa-cache"></i> `exchange_rate_cache.json` - Cache de tasa de cambio
- <i class="fas fa-moon"></i> `dark_mode_pref.json` - Preferencia de modo oscuro

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

1. <i class="fas fa-folder"></i> Crea la carpeta de configuraci&oacute;n oculta
2. <i class="fas fa-table"></i> Inicializa las tablas de la base de datos
3. <i class="fas fa-desktop"></i> Carga la interfaz gr&aacute;fica
4. <i class="fas fa-chart-line"></i> Muestra el Dashboard principal

### Navegaci&oacute;n

La barra lateral contiene las siguientes opciones:

| Bot&oacute;n | Icono | Vista |
|:---|:---|:---|
| <i class="fas fa-tachometer-alt"></i> | Dashboard | Panel ejecutivo |
| <i class="fas fa-shopping-cart"></i> | Ventas | Registro de ventas |
| <i class="fas fa-boxes"></i> | Productos | Gesti&oacute;n de inventario |
| <i class="fas fa-file-invoice"></i> | Facturas | Lista de facturas |
| <i class="fas fa-chart-line"></i> | Reportes | An&aacute;lisis de datos |
| <i class="fas fa-moon"></i>/<i class="fas fa-sun"></i> | Modo | Alternar tema |

---

## Tecnolog&iacute;as Utilizadas

| Tecnolog&iacute;a | Prop&oacute;sito | Versi&oacute;n |
|:---|:---|:---|
| <i class="fab fa-python"></i> **Python** | Lenguaje de programaci&oacute;n | 3.8+ |
| <i class="fab fa-flutter"></i> **Flet** | Framework de interfaz gr&aacute;fica | 0.21.0+ |
| <i class="fas fa-database"></i> **SQLite** | Base de datos embebida | 3.x |
| <i class="fas fa-paper-plane"></i> **Requests** | Cliente HTTP | 2.28+ |
| <i class="fas fa-file-pdf"></i> **FPDF** | Generaci&oacute;n de PDFs | 1.7+ |
| <i class="fas fa-file-excel"></i> **OpenPyXL** | Archivos Excel | 3.0+ |
| <i class="fas fa-chart-line"></i> **Flet Charts** | Gr&aacute;ficos | (incluido en Flet) |

---


## Contribuci&oacute;n

<i class="fas fa-hands-helping"></i> &iexcl;Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

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
| <i class="fas fa-user"></i> **Desarrollador** | Darkangel120 |
| <i class="fab fa-github"></i> **GitHub** | [github.com/Darkangel120](https://github.com/Darkangel120) |

---

## Agradecimientos

| | |
|:---|:---|
| <i class="fas fa-heart"></i> | Gracias por usar VentaEnterprise |
| <i class="fas fa-hands-helping"></i> | Contribuye al proyecto |
| <i class="fas fa-star"></i> | Dale una estrella en GitHub |

---

<p align="center">
  <strong>VentaEnterprise &copy; 2026</strong>
</p>

<p align="center">
  <img src="VP-logo.png" alt="Logo" width="32" height="32">
</p>

