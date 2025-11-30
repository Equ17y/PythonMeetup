from typing import List, Dict
from telegram import Bot
from ptb.events_data import get_next_events

# TODO: УДАЛИТЬ ВСЁ ЭТО ПРИ ПЕРЕХОДЕ НА БД - НАЧАЛО  ЗАГЛУШКИ
_subscribed_users: set = set()  # Все подписанные пользователи
_known_events: set = set()  # Мероприятия, которые уже известны системе


# TODO: УДАЛИТЬ ВСЁ ЭТО ПРИ ПЕРЕХОДЕ НА БД - КОНЕЦ  ЗАГЛУШКИ


async def subscribe_to_all_events(user_id: int, bot=None) -> dict:
    """
    ПОДПИСЫВАЕТ ПОЛЬЗОВАТЕЛЯ НА УВЕДОМЛЕНИЯ О НОВЫХ МЕРОПРИЯТИЯХ
    """
    try:
        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - НАЧАЛО  ЛОГИКИ
        _subscribed_users.add(user_id)
        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - КОНЕЦ  ЛОГИКИ

        return {
            'success': True,
            'message': "Вы подписались на уведомления о новых мероприятиях!",
        }

    except Exception as e:
        return {
            'success': False,
            'message': "Произошла ошибка при подписке. Попробуйте позже."
        }


async def notify_about_new_events(bot: Bot):
    """
    ОСНОВНАЯ ФУНКЦИЯ ДЛЯ УВЕДОМЛЕНИЙ О НОВЫХ МЕРОПРИЯТИЯХ
    Проверяет только НОВЫЕ мероприятия, добавленные после последней проверки
    """
    try:
        # Получаем текущие мероприятия
        current_events = get_next_events()
        current_event_ids = {event['id'] for event in current_events}

        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - Начало логики
        # Находим новые мероприятия (которых не было в прошлой проверке)
        new_event_ids = current_event_ids - _known_events

        if not new_event_ids or not _subscribed_users:
            # Обновляем список известных мероприятий
            _known_events.update(current_event_ids)
            return

        # Получаем информацию о новых мероприятиях
        new_events = [event for event in current_events if
                      event['id'] in new_event_ids]

        # Уведомляем всех подписчиков о новых мероприятиях
        for user_id in _subscribed_users:
            try:
                await send_new_events_notification(bot, user_id, new_events)
            except Exception:
                pass

        # Обновляем список известных мероприятий
        _known_events.update(current_event_ids)
        # TODO: УДАЛИТЬ ПРИ ПЕРЕХОДЕ НА БД - Конец логики

    except Exception:
        pass


async def send_new_events_notification(bot, user_id: int,
                                       new_events: List[dict]):
    """Отправляет уведомление о НОВЫХ мероприятиях"""
    try:
        message = "*НОВОЕ МЕРОПРИЯТИЕ!*\n\n"

        for event in new_events:
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


# TODO: УДАЛИТЬ ЭТУ ФУНКЦИЮ ПРИ ПЕРЕХОДЕ НА БД
async def is_user_subscribed(user_id: int, event_id: int) -> bool:
    return False


# ШАБЛОН ДЛЯ БУДУЩЕГО ПЕРЕХОДА НА БД
"""
# TODO: РАСКОММЕНТИРОВАТЬ ПРИ ПЕРЕХОДЕ НА БД

from asgiref.sync import sync_to_async
from meetup_core.models.Models import User, Event, EventSubscription
from datetime import datetime, timedelta

@sync_to_async
def subscribe_to_all_events_db(user_id: int, bot=None) -> dict:
    try:
        user, created = User.objects.get_or_create(tg_id=user_id)

        # Просто создаем запись о подписке пользователя
        subscription, created = EventSubscription.objects.get_or_create(
            user=user,
            defaults={'subscribed_at': datetime.now()}
        )

        return {
            'success': True, 
            'message': "Вы подписались на уведомления о новых мероприятиях!",
        }

    except Exception as e:
        return {'success': False, 'message': "Ошибка при подписке"}

@sync_to_async 
def notify_about_new_events_db(bot: Bot):
    try:
        # Получаем всех подписанных пользователей
        subscribed_users = User.objects.filter(eventsubscription__isnull=False).distinct()

        # Получаем мероприятия, созданные после последней проверки
        # В реальной системе нужно хранить время последней проверки
        new_events = Event.objects.filter(created_at__gte=datetime.now() - timedelta(hours=24))

        if not new_events.exists() or not subscribed_users.exists():
            return

        events_list = list(new_events)

        for user in subscribed_users:
            try:
                await send_new_events_notification_db(bot, user.tg_id, events_list)
            except Exception:
                pass

    except Exception:
        pass

async def send_new_events_notification_db(bot, user_id: int, new_events: List):
    try:
        message = "*НОВОЕ МЕРОПРИЯТИЕ!*\n\n"

        for event in new_events:
            time_str = f"{event.started_at.strftime('%H:%M')} - {event.ended_at.strftime('%H:%M')}"
            message += f"• *{event.name}*\n"
            message += f"  {event.event_date} {time_str}\n"
            message += f"  {event.organizer}\n\n"

        await bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')

    except Exception:
        pass
"""