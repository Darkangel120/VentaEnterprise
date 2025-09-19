import flet as ft
from src.database import create_tables
from src.views.views import main
import os
import subprocess

def run_app(page: ft.Page):
    # Crear carpeta oculta para archivos de configuración
    hidden_dir = ".ventaenterprise"
    os.makedirs(hidden_dir, exist_ok=True)
    subprocess.run(['attrib', '+h', hidden_dir], shell=True)
    create_tables(hidden_dir)
    main(page)

if __name__ == '__main__':
    ft.app(target=run_app)
