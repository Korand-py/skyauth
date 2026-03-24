import flet as ft
from datetime import *
import pyotp
import time
import json
import asyncio
import os
from flet import LocalAuthentication
keys = "keys.json"

print(f"Flet version from package: {ft.__version__}")

async def main(page: ft.Page):
    print("Приложение запущено")
    page.title = "SkyAuth"
    page.window.width = 350
    page.window.min_height = 300
    page.window.resizable = False
    page.window.full_screen = False
    page.window.icon = "/logo_app.ico"
    page.bgcolor = "#000000"
    page.adaptive = True
    page.theme_mode = ft.ThemeMode.DARK
    
    # Основные переменные
    data = "keys.json"
    Protection_status = True
    # --- Загрузка данных из JSON ---
    def load_data():
        if os.path.exists(keys):
            try:
                with open(keys, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    # --- Сохранение данных в JSON ---
    def save_data(data_to_save):
        with open(keys, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

    # Загружаем данные
    data = load_data()

    # Блок уведомлений (по умолчанию кол-во ключей)
    count_keys = ft.Chip(label=ft.Text(f"Всего ключей: {len(data)}", size=18), leading=ft.Icon(
        icon=ft.Icons.KEY), color=ft.Colors.GREY_900)
    
    
    
    # --- Поля формы ---
    tb1 = ft.TextField(label="Сервис", width=250, color=ft.Colors.GREY)
    tb2 = ft.TextField(label="2FA ключ",
                       color=ft.Colors.GREY,
                       hint_text="Пример: JBSWY3DPEHPK3PXP",
                       width=250)
    
    # --- Функция добавления ключа ---
    def add_key(e):
        service = tb1.value.strip()
        secret_key = tb2.value.strip()
        
        if not service or not secret_key:
            snack_bar = ft.SnackBar(ft.Text("Заполните все поля", color=ft.Colors.WHITE))
            snack_bar.open = True
            page.update()
            return
        
        try:
            time_key = time.time()
            new_item = {
                'service': service,
                'secret_key': secret_key,
                'last_update': time.ctime(time_key)
            }
            
            data.append(new_item)
            save_data(data)
            
            dialog_add_key.open = False
            tb1.value = ""
            tb2.value = ""
            update_cards()
            page.update()
            
        except Exception as ex:
            print(f"Ошибка: {ex}")
            snack_bar = ft.SnackBar(
                ft.Text("Ошибка при добавлении ключа", color=ft.Colors.WHITE), 
                bgcolor=ft.Colors.RED
            )
            snack_bar.open = True
            dialog_add_key.open = False
            page.update()
            
    # --- Диалог добавления ключа (создаем с содержимым сразу) ---
    dialog_add_key = ft.AlertDialog(
        modal=True,
        shape=ft.RoundedRectangleBorder(
        radius=10,
        side=ft.BorderSide(width=2, color=ft.Colors.BLUE_400)
        ),
        bgcolor=ft.Colors.SURFACE,
        title=ft.Text("Добавить ключ", color=ft.Colors.ON_SURFACE),
        content=ft.Column([
            ft.Icon(ft.Icons.KEY, color=ft.Colors.GREY, size=40),
            tb1,
            tb2,
            ft.Row([
                ft.Button(
                    "Добавить",
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                    on_click=add_key
                ),
                ft.Button(
                    "Отмена",
                    bgcolor=ft.Colors.RED,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: setattr(dialog_add_key, 'open', False)
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], tight=True, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    
    # --- Кнопка открытия диалога добавления ключа ---
    add_key_button = ft.IconButton(
        icon=ft.Icons.ADD,
        bgcolor="#1048FF",
        icon_color="#FFFFFF",
        scale=1.5,
        on_click=lambda e: setattr(dialog_add_key, 'open', True)
    )
    
    # --- Функция обновления всех ключей ---
    async def update_all(e):
        time_key = time.time()
        for k in range(len(data)):
            data[k]["last_update"] = time.ctime(time_key)
        save_data(data)
        update_cards()
        
        count_keys.label = ft.Text("Все ключи обновились", sizFe=18)
        page.update()
        await asyncio.sleep(3)
        count_keys.label = ft.Text(f"Всего ключей: {len(data)}", size=18)
        page.update()
    
    button_update_all = ft.IconButton(
        icon=ft.Icons.UPDATE,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda e: page.run_task(update_all, e)
    )
    
    #? --- Функции для карточек ---
    def delete_card(e, index):
        if 0 <= index < len(data):
            data.pop(index)
            save_data(data)
            update_cards()
            page.update()
    
    def create_card_code(item, index):
        try:
            totp = pyotp.TOTP(item["secret_key"])
            code = totp.now()
            return ft.Card(bgcolor=ft.Colors.ON_SURFACE,
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(item["service"], size=20, weight=ft.FontWeight.BOLD, expand=True),
                            ft.Text(f"{code}", size=20, color=ft.Colors.BLUE, selectable=True),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                bgcolor=ft.Colors.TRANSPARENT,
                                on_click=lambda e, idx=index: delete_card(e, idx),
                                icon_size=20,
                                disabled=Protection_status
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Обновлено: {item['last_update']}", size=12, color=ft.Colors.GREY_500)
                    ]),
                    padding=10,
                    width=300,
                    bgcolor="#161515",
                    border_radius=10
                ),
                elevation=5,
                margin=10,
                
                
            )
        except:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"   Ошибка ключа: {item['service']}", color=ft.Colors.RED),
                        ft.Text("Неверный формат ключа", size=12, color=ft.Colors.RED),
                        ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                bgcolor=ft.Colors.TRANSPARENT,
                                on_click=lambda e, idx=index: delete_card(e, idx),
                                icon_size=20,
                                disabled=False,
                                alignment=ft.Alignment.BOTTOM_RIGHT
                            )
                    ]),
                    width=300,
                    border_radius=10,
                    bgcolor="#161515",
                )
            )
    
    # * --- Обновление карточек ---
    def update_cards():
        cards_column.controls.clear()
        for i, item in enumerate(data):
            card = create_card_code(item, i)
            cards_column.controls.append(card)
        
        if not data:
            cards_column.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.KEY_OFF, size=50, color=ft.Colors.GREY_500),
                        ft.Text("Ключей нет...", size=20, color=ft.Colors.GREY_500)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=20
                )
            )
        
        count_keys.label = f"Всего ключей: {len(data)}"
        cards_column.update()
    
    # --- Контейнер для карточек ---
    cards_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # --- Переключатель защиты ---
    
    switch_protection = ft.Switch(
    value=Protection_status,
    active_color=ft.Colors.BLUE,
    on_change=lambda e: toggle_protection(e))

    def toggle_protection(e):
        nonlocal Protection_status
    
    # Получаем новое значение из переключателя
        Protection_status = switch_protection.value
    
    # Обновляем только отображение кнопок удаления
        update_cards()
    
    # Обновляем состояние кнопки удаления всех кодов
        delete_all_codes_button.disabled = Protection_status



    # --- Функция удаления всех кодов ---
    async def delete_all_codes(e):
        data.clear()
        save_data(data)
        update_cards()
        setting_dialog.open = False
        delete_all_codes_button.disabled = Protection_status
        count_keys.label = ft.Text("Все ключи удалены", size=18)
        page.update()
        await asyncio.sleep(3)
        count_keys.label = ft.Text(f"Всего ключей: {len(data)}", size=18)
        page.update()
    
    delete_all_codes_button = ft.IconButton(
                icon=ft.Icons.DELETE_FOREVER,
                icon_color=ft.Colors.RED,
                on_click=lambda e: page.run_task(delete_all_codes, e),
                disabled=Protection_status
            )

    # --- Скачивание и загрузка файла keys.json
        # --- в Beta 1.1.0
    global content_text
    content_text = ""
    def open_keys_dialog(e):
        keys_file = "keys.json"
    # Читаем файл ПРИ КАЖДОМ открытии диалога
        if os.path.exists(keys_file):
            try:
                with open(keys_file, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    content_text = json.dumps(file_data, ensure_ascii=False, indent=2)
            except Exception as ex:
                content_text = f"Ошибка чтения файла: {ex}"
        else:
            content_text = "Файл не найден"
    
    # Обновляем текст в диалоге
        dialog_file_key.content.content.value = content_text
        setting_dialog.open = False
        dialog_file_key.open = True
        page.update()

    dialog_file_key = ft.AlertDialog(
        title=ft.Row([ft.Text("keys.json")]),
        modal=True,
        bgcolor=ft.Colors.SURFACE,
        shape=ft.RoundedRectangleBorder(
            radius=10,
            side=ft.BorderSide(width=2, color=ft.Colors.BLUE_400)
        ),
        content=ft.Container(
            content=ft.Text(
                content_text, 
                selectable=True,
                size=12
            ),
            padding=15,
            bgcolor=ft.Colors.BLACK_12,
            border_radius=8,
            width=400,
            height=300,
        ),
        actions=[
            ft.TextButton(
                "Закрыть", 
                on_click=lambda e: setattr(dialog_file_key, 'open', False),
                style=ft.ButtonStyle(color=ft.Colors.BLUE)
            )
        ]
    )
    # --- Диалог настроек ---
    setting_dialog = ft.AlertDialog(
    modal=True,
    shape=ft.RoundedRectangleBorder(
        radius=10,
        side=ft.BorderSide(width=2, color=ft.Colors.BLUE_400)
    ),
    bgcolor=ft.Colors.SURFACE,
    title=ft.Text("Настройки", color=ft.Colors.ON_SURFACE),
    content=ft.Column([
        ft.Row([
            ft.Text("Режим защиты", size=16, expand=True, color=ft.Colors.ON_SURFACE),
            switch_protection
        ]),
        ft.Divider(height=20),
        ft.Row([
            ft.Text("Скачать все коды", size=16, expand=True, color=ft.Colors.ON_SURFACE),
            ft.IconButton(
                icon=ft.Icons.DOWNLOAD,
                icon_color=ft.Colors.GREEN,
                bgcolor=ft.Colors.TRANSPARENT,
                on_click=lambda e: open_keys_dialog(None)
)
        ]),
        ft.Divider(height=20),
        ft.Row([
            ft.Text("Удалить все коды", size=16, expand=True, color=ft.Colors.ON_SURFACE),
            delete_all_codes_button
        ]),
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ft.Text("SkyAuth Beta v1.1", size=12, color=ft.Colors.GREY_500)
    ], width=300, height=200),
    actions=[
        ft.TextButton(
            "Закрыть", 
            on_click=lambda e: setattr(setting_dialog, 'open', False),
            style=ft.ButtonStyle(color=ft.Colors.BLUE)
        )
    ]
)
    
    # --- Кнопка настроек ---
    button_settings = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda e: setattr(setting_dialog, 'open', True)
    )
    

    page.overlay.extend([dialog_add_key, setting_dialog, dialog_file_key])
    
    main_content = ft.Column([
    ft.Image(src="assets/icon_app.png", width=80, height=80),
    ft.Divider(height=12, color=ft.Colors.TRANSPARENT),
    count_keys,
    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
    # ОСНОВНОЙ КОНТЕНТ (карточки)
    ft.Container(
        content=cards_column,
        expand=True,  
        padding=10,
        bgcolor=ft.Colors.BLACK, 
    ),
    # ПАНЕЛЬ КНОПОК ВНИЗУ
    ft.Container(
        content=ft.Column([
            ft.Row([
                button_settings,
                add_key_button,
                button_update_all
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20), ft.Divider(height=12, color=ft.Colors.TRANSPARENT)
        ],
        spacing=25,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        bgcolor=ft.Colors.TRANSPARENT
    )
],
spacing=0,
expand=True,
horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    page.add(main_content)
    update_cards()
    page.update()
    
ft.app(
    target=main,
    assets_dir="assets",
    view=ft.AppView.FLET_APP,
    name="SkyAuth"
    
)