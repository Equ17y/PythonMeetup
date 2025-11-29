import asyncio
from datetime import datetime
from telegram import Bot
from .subscription_service import get_event_subscribers, send_event_booklet


async def send_reminders(bot: Bot):
    """Отправляет напоминания с буклетами мероприятий"""
    current_time = datetime.now().strftime("%H:%M:%S")
    # TODO: УДАЛИТЬ принт при итоговой сдаче
    print(f"[{current_time}] Сервис напоминаний проверяет события...")

    # # TODO: ЗАМЕНИТЬ на get_events_for_reminders() при переходе на БД
    test_events = [
        {"id": 1, "name": "Python Meetup #1"},
        {"id": 2, "name": "Python Meetup #2"},
        {"id": 3, "name": "Python Meetup #3"}
    ]

    total_sent = 0

    for event in test_events:
        subscribers = await get_event_subscribers(event["id"])

        # TODO: УДАЛИТЬ принт
        print(
            f"Мероприятие '{event['name']}': {len(subscribers)} подписчиков")

        for user_id in subscribers:
            try:
                from ptb.services.subscription_service import \
                    send_event_booklet
                await send_event_booklet(bot, user_id, event["id"])

                print(f"Буклет отправлен пользователю {user_id}")
                total_sent += 1
            except Exception as e:
                print(f"Ошибка отправки буклета {user_id}: {e}")

    # TODO: УДАЛИТЬ принт
    print(f"Итого отправлено: {total_sent} буклетов")


async def start_reminder_service(bot: Bot):
    """Запуск сервиса напоминаний"""
    print("Сервис напоминаний запущен!")

    # Первая проверка через 30 секунд после запуска
    await asyncio.sleep(30)
    await send_reminders(bot)

    while True:
        await asyncio.sleep(60)  # Проверка каждые 1 минуты
        await send_reminders(bot)