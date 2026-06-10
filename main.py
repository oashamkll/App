import flet as ft
from telethon import TelegramClient
import asyncio
import os

# Инициализируем клиент глобально
client = None

def main(page: ft.Page):
    page.title = "TeleBot Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30
    
    global client
    
    # Session state
    api_id = ""
    api_hash = ""
    phone = ""
    phone_code_hash = ""

    # Ввод данных
    api_id_input = ft.TextField(label="API ID", width=320, border_radius=15, prefix_icon=ft.icons.VKEY)
    api_hash_input = ft.TextField(label="API HASH", width=320, password=True, can_reveal_password=True, border_radius=15, prefix_icon=ft.icons.PASSWORD)
    phone_input = ft.TextField(label="Номер телефона (+123...)", width=320, border_radius=15, prefix_icon=ft.icons.PHONE)
    code_input = ft.TextField(label="Код из Telegram", width=320, border_radius=15, prefix_icon=ft.icons.NUMBERS, visible=False)

    status_text = ft.Text("Введите данные для входа", color=ft.colors.GREY_400, text_align=ft.TextAlign.CENTER)

    # --- DASHBOARD UI ---
    dashboard_col = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    
    def on_ping_click(e):
        asyncio.create_task(ping_action())

    async def ping_action():
        try:
            global client
            await client.send_message("me", "👋 Привет от UserBot! Я успешно запущен и работаю.")
            show_snack("Пинг отправлен в Избранное!", ft.colors.GREEN_700)
        except Exception as ex:
            show_snack(f"Ошибка: {ex}", ft.colors.RED_700)

    def on_parse_click(e):
        asyncio.create_task(parse_action())

    async def parse_action():
        try:
            global client
            dialogs = await client.get_dialogs(limit=10)
            chat_names = [d.name for d in dialogs if d.is_group or d.is_channel]
            if chat_names:
                msg = "Ваши чаты: " + ", ".join(chat_names[:3]) + "..."
                show_snack(msg, ft.colors.GREEN_700)
            else:
                show_snack("Групп не найдено.", ft.colors.ORANGE_700)
        except Exception as ex:
            show_snack(f"Ошибка: {ex}", ft.colors.RED_700)

    btn1 = ft.ElevatedButton("📩 Отправить пинг в Избранное", icon=ft.icons.MESSAGE, width=320, height=50, on_click=on_ping_click)
    btn2 = ft.ElevatedButton("👥 Спарсить список чатов", icon=ft.icons.LIST_ALT, width=320, height=50, on_click=on_parse_click)
    
    dashboard_col.controls.extend([
        ft.Text("Управление аккаунтом", size=24, weight=ft.FontWeight.BOLD),
        btn1, btn2
    ])

    def show_snack(msg, color):
        page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # --- LOGIN LOGIC ---
    login_col = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)

    def request_code_click(e):
        asyncio.create_task(request_code_action())

    async def request_code_action():
        nonlocal api_id, api_hash, phone, phone_code_hash
        global client
        
        if not api_id_input.value or not api_hash_input.value or not phone_input.value:
            status_text.value = "Ошибка: заполните все поля!"
            status_text.color = ft.colors.RED_400
            page.update()
            return

        try:
            api_id = int(api_id_input.value)
            api_hash = api_hash_input.value
            phone = phone_input.value
            
            session_path = os.path.join(page.client_storage.get_path(), "userbot.session") if hasattr(page.client_storage, "get_path") else "userbot.session"
            client = TelegramClient(session_path, api_id, api_hash)
            await client.connect()
            
            if not await client.is_user_authorized():
                result = await client.send_code_request(phone)
                phone_code_hash = result.phone_code_hash
                
                status_text.value = "Код отправлен в Telegram!"
                status_text.color = ft.colors.ORANGE_400
                code_input.visible = True
                req_btn.visible = False
                login_btn.visible = True
                page.update()
            else:
                show_dashboard()
        except Exception as ex:
            status_text.value = f"Ошибка: {ex}"
            status_text.color = ft.colors.RED_400
            page.update()

    def login_click(e):
        asyncio.create_task(login_action())

    async def login_action():
        nonlocal phone, phone_code_hash
        global client
        if not code_input.value:
            return
            
        try:
            await client.sign_in(phone, code_input.value, phone_code_hash=phone_code_hash)
            show_dashboard()
        except Exception as ex:
            status_text.value = f"Ошибка кода: {ex}"
            status_text.color = ft.colors.RED_400
            page.update()

    def show_dashboard():
        status_text.value = "Успешная авторизация!"
        status_text.color = ft.colors.GREEN_400
        login_col.visible = False
        dashboard_col.visible = True
        page.update()

    req_btn = ft.ElevatedButton("Запросить код", on_click=request_code_click, width=320, height=50, 
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE))
    
    login_btn = ft.ElevatedButton("Войти", on_click=login_click, width=320, height=50, visible=False,
                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15), bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE))

    login_col.controls.extend([
        api_id_input,
        api_hash_input,
        phone_input,
        code_input,
        req_btn,
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
