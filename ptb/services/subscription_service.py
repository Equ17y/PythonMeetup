from typing import List, Dict
from telegram import Bot
from ptb.events_data import get_next_events

# TODO: УДАЛИТЬ ВСЁ ЭТО ПРИ ПЕРЕХОДЕ НА БД - НАЧАЛО ЛОКАЛЬНОЙ ЗАГЛУШКИ
_subscribed_users: set = set()  # Все пользователи с любой подпиской


# TODO: УДАЛИТЬ ВСЁ ЭТО ПРИ ПЕРЕХОДЕ НА БД - КОНЕЦ ЛОКАЛЬНОЙ ЗАГЛУШКИ


async def subscribe_to_all_events(user_id: int, bot=None) -> dict:
    """
    ПОДПИСЫВАЕТ ПОЛЬЗОВАТЕЛЯ НА ВСЕ БУДУЩИЕ МЕРОПРИЯТИЯ
    """
    try:
        events = get_next_events()

        if not events:
            return {
                'success': False,
                'message': "На данный момент нет доступных мероприятий для подписки."
            }

        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - НАЧАЛО ЛОКАЛЬНОЙ ЛОГИКИ
        _subscribed_users.add(user_id)

        if bot:
            await send_events_notification(bot, user_id, events)
        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - КОНЕЦ ЛОКАЛЬНОЙ ЛОГИКИ

        return {
            'success': True,
            'message': f"Вы подписались на {len(events)} будущих мероприятий!",
            'subscribed_count': len(events)
        }

    except Exception as e:
        return {
            'success': False,
            'message': "Произошла ошибка при подписке. Попробуйте позже."
        }


async def send_events_notification(bot, user_id: int, events: List[dict]):
    """Отправляет уведомление о мероприятиях"""
    try:
        message = "*НОВЫЕ МЕРОПРИЯТИЯ!*\n\n"

        for event in events:
            time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"
            message += f"• *{event['name']}*\n"
            message += f"  {event['event_date']} {time_str}\n"
            message += f"  {event.get('organizer', 'Иван Петров')}\n\n"

        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode='Markdown'
        )

    except Exception:
        pass


async def notify_about_new_events(bot: Bot):
    """
    ОСНОВНАЯ ФУНКЦИЯ ДЛЯ УВЕДОМЛЕНИЙ О НОВЫХ МЕРОПРИЯТИЯХ
    Вызывается из reminder_service.py
    """
    try:
        events = get_next_events()

        if not events:
            return

        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД
        if not _subscribed_users:
            return

        for user_id in _subscribed_users:
            try:
                await send_events_notification(bot, user_id, events)
            except Exception:
                pass

    except Exception:
        pass


# TODO: УДАЛИТЬ ЭТУ ФУНКЦИЮ ПРИ ПЕРЕХОДЕ НА БД
async def is_user_subscribed(user_id: int, event_id: int) -> bool:
    """Проверяет подписку (временная функция для совместимости)"""
    return False


# ШАБЛОН ДЛЯ БУДУЩЕГО ПЕРЕХОДА НА БД
"""
# TODO: РАСКОММЕНТИРОВАТЬ ПРИ ПЕРЕХОДЕ НА БД

from asgiref.sync import sync_to_async
from meetup_core.models.Models import User, Event, EventSubscription
from datetime import datetime

@sync_to_async
def subscribe_to_all_events_db(user_id: int, bot=None) -> dict:
    try:
        user, created = User.objects.get_or_create(tg_id=user_id)
        future_events = Event.objects.filter(event_date__gte=datetime.now().date())

        if not future_events.exists():
            return {'success': False, 'message': "Нет доступных мероприятий"}

        for event in future_events:
            EventSubscription.objects.get_or_create(user=user, event=event)

        if bot:
            events_list = list(future_events)
            await send_events_notification_db(bot, user_id, events_list)

        return {
            'success': True, 
            'message': f"Вы подписались на {future_events.count()} будущих мероприятий!",
            'subscribed_count': future_events.count()
        }

    except Exception as e:
        return {'success': False, 'message': "Ошибка при подписке"}

async def send_events_notification_db(bot, user_id: int, events: List):
    try:
        message = "*НОВЫЕ МЕРОПРИЯТИЯ!*\n\n"

        for event in events:
            time_str = f"{event.started_at.strftime('%H:%M')} - {event.ended_at.strftime('%H:%M')}"
            message += f"• *{event.name}*\n"
            message += f"  {event.event_date} {time_str}\n"
            message += f"  {event.organizer}\n\n"

        await bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')

    except Exception:
        pass

@sync_to_async 
def notify_about_new_events_db(bot: Bot):
    try:
        subscribed_users = User.objects.filter(eventsubscription__isnull=False).distinct()
        future_events = Event.objects.filter(event_date__gte=datetime.now().date())

        if not future_events.exists() or not subscribed_users.exists():
            return

        events_list = list(future_events)

        for user in subscribed_users:
            try:
                await send_events_notification_db(bot, user.tg_id, events_list)
            except Exception:
                pass

    except Exception:
        pass
"""