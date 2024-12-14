import flet as ft
import sqlite3
import time


# Шаблон для создания адаптивных окон
def create_view(route, title, controls, bgcolor="white"):
    return ft.View(
        route,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(title, size=24, weight="bold", text_align="center"),
                        *controls  # Все элементы, переданные в controls
                    ],
                    alignment="center",
                    spacing=20,
                ),
                bgcolor=bgcolor,  # Цвет фона
                padding=20,
                border_radius=10,
                expand=True,  # Сделать контейнер адаптивным
                alignment=ft.alignment.center  # Центрирование содержимого
            )
        ],
    )

# Шаблон для главного меню
def main_menu(route, title, controls, bgcolor="white"):
    return ft.View(
        route,
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(title, size=24, weight="bold", text_align="center"),
                        *controls  # Все элементы, переданные в controls
                    ],
                    alignment="center",
                    spacing=20,
                ),
                bgcolor=bgcolor,  # Цвет фона
                padding=20,
                border_radius=10,
                expand=True,  # Сделать контейнер адаптивным
                alignment=ft.alignment.center  # Центрирование содержимого
            )
        ],
    )

def main(page: ft.Page):
    # Установка размеров страницы с учетом адаптивности
    page.horizontal_alignment = ft.alignment.center
    page.vertical_alignment = ft.alignment.center

    # Подключение к базе данных SQLite
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    # Создание таблицы для хранения номеров телефонов
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT
        )
    """)
    conn.commit()

    # Функция сохранения номера телефона
    def save_phone_number(e):
        phone_number = phone_field.value.strip()
        if phone_number:
            try:
                cursor.execute("INSERT INTO users (phone_number) VALUES (?)", (phone_number,))
                conn.commit()
                page.snack_bar = ft.SnackBar(ft.Text("Номер сохранён!"))
                phone_field.value = ""
            except sqlite3.Error as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка сохранения: {err}"))
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Введите номер телефона!"))
        page.snack_bar.open()
        page.update()

    # Переход к экрану настроек
    def go_to_settings(e):
        try:
            cursor.execute("SELECT phone_number FROM users ORDER BY id DESC LIMIT 1")
            user = cursor.fetchone()
            user_phone = user[0] if user else "Не задан"
        except sqlite3.Error as err:
            user_phone = f"Ошибка загрузки данных: {err}"

        settings_view = create_view(
            route="/settings",
            title="Настройки",
            controls=[
                ft.Text(f"Ваш номер телефона: {user_phone}", size=18),
                ft.ElevatedButton("Назад", on_click=go_back)
            ],
            bgcolor="lightblue"
        )
        page.views.append(settings_view)
        page.go("/settings")

    # Функция возврата на главный экран
    def go_back(e):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)

    # Функция отображения загрузочного экрана
    def show_loading_screen():
        loading_view = create_view(
            route="/loading",
            title="Загрузка...",
            controls=[ft.ProgressRing()],
            bgcolor="lightgray"
        )
        page.views.append(loading_view)
        page.update()
        time.sleep(2)  # Имитация задержки загрузки данных
        page.views.pop()
        page.views.append(registration_view)
        page.update()

    # Элемент для ввода номера телефона
    phone_field = ft.TextField(
        label="Введите номер телефона",
        hint_text="XX XXX-XX-XX",
        prefix_text="+998 ",
        width=300
    )

    # Кнопки для сохранения и перехода к настройкам
    save_button = ft.ElevatedButton("Сохранить номер", on_click=save_phone_number)
    settings_button = ft.ElevatedButton("Перейти к настройкам", on_click=go_to_settings)

    # Главный экран регистрации
    registration_view = create_view(
        route="/",
        title="Регистрация пользователя",
        controls=[
            phone_field,
            save_button,
            settings_button
        ],
        bgcolor="lightblue"
    )

    # Отображение загрузочного экрана при запуске
    show_loading_screen()


# Запуск приложения
ft.app(target=main)
