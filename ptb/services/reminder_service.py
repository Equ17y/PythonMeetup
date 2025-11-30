import asyncio
from telegram import Bot
from .subscription_service import notify_about_new_events


async def send_reminders(bot: Bot):
    """ОСНОВНАЯ ФУНКЦИЯ РАССЫЛКИ"""
    await notify_about_new_events(bot)


async def start_reminder_service(bot: Bot):
    """Запуск сервиса уведомлений"""
    await asyncio.sleep(30)
    await send_reminders(bot)

    while True:
        await asyncio.sleep(60)
        await send_reminders(bot)