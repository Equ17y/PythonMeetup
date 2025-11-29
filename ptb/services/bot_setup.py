from telegram.ext import Application
from ptb.handlers.conversation_handlers import conversation_handler
from .reminder_service import start_reminder_service
import asyncio


def setup_bot_handlers(application: Application):
    """Настройка всех обработчиков бота"""
    print("🛠 Настройка обработчиков бота...")
    application.add_handler(conversation_handler)
    print("✅ Обработчики настроены")


def start_background_services(application: Application):
    """Запуск фоновых сервисов"""
    print("🔄 Запуск фоновых сервисов...")
    bot = application.bot
    loop = asyncio.get_event_loop()
    loop.create_task(start_reminder_service(bot))
    print("✅ Фоновые сервисы запущены")
