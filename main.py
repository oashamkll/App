import flet as ft
import asyncio

def main(page: ft.Page):
    page.title = "TeleBot Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    api_id_input = ft.TextField(label="API ID", width=320, border_radius=15, prefix_icon=ft.icons.VKEY)
    api_hash_input = ft.TextField(label="API HASH", width=320, password=True, can_reveal_password=True, border_radius=15, prefix_icon=ft.icons.PASSWORD)
    phone_input = ft.TextField(label="Номер телефона (+123...)", width=320, border_radius=15, prefix_icon=ft.icons.PHONE)

    status_text = ft.Text("Введите данные для входа", color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER)

    dashboard_col = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    
    def btn_action(e):
        page.snack_bar = ft.SnackBar(ft.Text(f"Функция '{e.control.text}' выполнена успешно!"), bgcolor=ft.colors.GREEN_700)
        page.snack_bar.open = True
        page.update()

    btn1 = ft.ElevatedButton("📩 Отправить пинг в Избранное", icon=ft.icons.MESSAGE, width=320, height=50, on_click=btn_action)
    def scrape_users_action(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("Функция парсинга запущена (требуется подключение Telethon)"), 
            bgcolor=ft.colors.ORANGE_700
        )
        page.snack_bar.open = True
        page.update()

    btn2 = ft.ElevatedButton("👥 Спарсить список чатов и участников", icon=ft.icons.LIST_ALT, width=320, height=50, on_click=scrape_users_action)
    btn3 = ft.ElevatedButton("⚙️ Настроить автоответчик", icon=ft.icons.REPLY_ALL, width=320, height=50, on_click=btn_action)
    btn4 = ft.ElevatedButton("🧹 Очистить кэш", icon=ft.icons.CLEANING_SERVICES, width=320, height=50, on_click=btn_action)
    
    dashboard_col.controls.extend([
        ft.Text("Управление аккаунтом", size=24, weight=ft.FontWeight.BOLD),
        btn1, btn2, btn3, btn4
    ])

    login_col = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    def login_click(e):
        if not api_id_input.value or not api_hash_input.value or not phone_input.value:
            status_text.value = "Ошибка: заполните все поля!"
            status_text.color = ft.colors.RED_400
            page.update()
            return

        status_text.value = "Успешная авторизация!"
        status_text.color = ft.colors.GREEN_400
        
        login_col.visible = False
        dashboard_col.visible = True
        page.update()

    login_btn = ft.ElevatedButton("Войти в аккаунт", on_click=login_click, width=320, height=50, 
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE))

    login_col.controls.extend([
        api_id_input,
        api_hash_input,
        phone_input,
        login_btn,
        status_text
    ])

    page.add(
        ft.Container(
            content=ft.Image(src="icon.png", width=120, height=120, fit=ft.ImageFit.CONTAIN, border_radius=20),
            margin=ft.margin.only(bottom=10)
        ),
        ft.Text("UserBot App", size=32, weight=ft.FontWeight.BOLD),
        ft.Text("Telethon Powered", size=14, color=ft.colors.BLUE_300),
        ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        login_col,
        dashboard_col
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
