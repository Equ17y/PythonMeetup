import asyncio
from datetime import datetime
from telegram import Bot
from .subscription_service import get_event_subscribers


async def send_test_reminder(bot: Bot, user_id: int, event_name: str):
    """Отправляет тестовое напоминание"""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=f"🔔 *Тестовое напоминание!*\n\nМероприятие: *{event_name}*\n\nЭто тестовое сообщение системы напоминаний.",
            parse_mode='Markdown'
        )
        print(f"Тестовое напоминание отправлено пользователю {user_id}")
    except Exception as e:
        print(f"Ошибка отправки напоминания {user_id}: {e}")


async def send_reminders(bot: Bot):
    """Тестовые напоминания (заглушка)"""
    print("🔔 Сервис напоминаний проверяет события...")

    # Тестовые мероприятия для демонстрации
    test_events = [
        {"id": 1, "name": "Python Meetup #1"},
        {"id": 2, "name": "Python Meetup #2"},
        {"id": 3, "name": "Python Meetup #3"}
    ]

    for event in test_events:
        subscribers = await get_event_subscribers(event["id"])

        print(
            f"Мероприятие '{event['name']}': {len(subscribers)} подписчиков")

        for user_id in subscribers:
            await send_test_reminder(bot, user_id, event["name"])
            # В реальности здесь будет проверка даты и отправка за день до мероприятия


async def start_reminder_service(bot: Bot):
    """Запуск сервиса напоминаний"""
    print("🚀 Сервис напоминаний запущен!")
    print(f"🕒 Время запуска: {datetime.now()}")

    # Первая проверка через 30 секунд после запуска
    print("⏰ Ожидаем 30 секунд до первой проверки...")
    await asyncio.sleep(30)
    print("🔔 Первая проверка напоминаний...")
    await send_reminders(bot)

    # Дальше проверяем каждые 2 минуты для демонстрации
    counter = 1
    while True:
        counter += 1
        print(f"🔄 Цикл #{counter}: ожидаем 120 секунд...")
        await asyncio.sleep(120)  # 2 минуты
        print(f"🔔 Проверка напоминаний #{counter}...")
        await send_reminders(bot)