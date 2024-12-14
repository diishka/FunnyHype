import flet as ft

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

def main(page: ft.Page):
    # Функции для перехода на разные страницы
    def go_home(e):
        page.go("/home")
    
    def go_profile(e):
        page.go("/profile")

    def go_cart(e):
        page.go("/cart")

    # Главная страница
    home_view = create_view(
        route="/home",
        title="Главная страница",
        controls=[ft.Text("Добро пожаловать на главную страницу!")],
        bgcolor="lightblue"
    )

    # Страница профиля
    profile_view = create_view(
        route="/profile",
        title="Профиль",
        controls=[ft.Text("Здесь будет информация о профиле.")],
        bgcolor="lightgreen"
    )

    # Страница корзины
    cart_view = create_view(
        route="/cart",
        title="Корзина",
        controls=[ft.Text("Ваша корзина пуста.")],
        bgcolor="lightyellow"
    )

    # Панель навигации (navbar)
    navbar = ft.Row(
        controls=[
            ft.IconButton(ft.icons.HOME, on_click=go_home),
            ft.IconButton(ft.icons.GRID_VIEW, on_click=go_cart),
            ft.IconButton(ft.icons.SHOPPING_CART, on_click=go_cart),
            ft.ElevatedButton("Профиль", on_click=go_profile)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    # Главная страница с navbar
    page.add(home_view, navbar)
    page.update()

# Запуск приложения
ft.app(target=main)
