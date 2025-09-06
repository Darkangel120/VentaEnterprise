import flet as ft
from src.database import create_tables
from src.views.views import main

def run_app(page: ft.Page):
    create_tables()
    main(page)

if __name__ == '__main__':
    ft.app(target=run_app)
