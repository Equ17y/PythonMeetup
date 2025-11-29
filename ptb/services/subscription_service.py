from typing import List, Dict
from ptb.events_data import get_next_events, get_next_event_program

# ВРЕМЕННО: заглушка вместо БД
# TODO: УДАЛИТЬ при переходе на БД
_subscriptions: Dict[int, List[int]] = {}  # {user_id: [event_ids]}


async def subscribe_to_event(user_id: int, event_id: int, bot=None) -> bool:
    """Подписывает пользователя на мероприятие (заглушка)"""
    # TODO: УДАЛИТЬ принты перед итогвоой сдаче
    print(f"🔔 Подписка: пользователь {user_id} на мероприятие {event_id}")

    if user_id not in _subscriptions:
        _subscriptions[user_id] = []

    if event_id not in _subscriptions[user_id]:
        _subscriptions[user_id].append(event_id)
        # TODO: УДАЛИТЬ принт
        print(
            f"Пользователь {user_id} подписан на мероприятие {event_id}")

        if bot:
            await send_event_booklet(bot, user_id, event_id)

        return True

    # TODO: УДАЛИТЬ принт
    print(
        f"Пользователь {user_id} уже подписан на мероприятие {event_id}")
    return False


async def send_event_booklet(bot, user_id: int, event_id: int):
    """Отправляет буклет с информацией о мероприятии"""
    try:
        # Получаем информацию о мероприятии
        events = get_next_events()
        event = next((e for e in events if e['id'] == event_id), None)

        if not event:
            # TODO: УДАЛИТЬ принт
            print(f"Мероприятие {event_id} не найдено для буклета")
            return

        # Получаем программу мероприятия
        program = get_next_event_program(event_id)

        # Формируем буклет
        booklet_text = format_event_booklet(event, program)

        # Отправляем буклет пользователю
        await bot.send_message(
            chat_id=user_id,
            text=booklet_text,
            parse_mode='Markdown'
        )
        print(
            f"Буклет отправлен пользователю {user_id} для мероприятия {event_id}")

    except Exception as e:
        print(f" Ошибка отправки буклета пользователю {user_id}: {e}")


def format_event_booklet(event, program) -> str:
    """
    Форматирует буклет с информацией о мероприятии
    """
    booklet = "*ПРОГРАММА МЕРОПРИЯТИЯ*\n\n"

    # Программа
    if program:
        for i, session in enumerate(program, 1):
            booklet += f"{i}. *{session['topic']}*\n"
            booklet += f"{session['started_at']} - {session['ended_at']}\n"
            booklet += f"Докладчик: {session['speaker']}\n"

            # Добавляем username если есть
            if session.get('speaker_username'):
                booklet += f"@{session['speaker_username'].lstrip('@')}\n"

            booklet += "\n"
    else:
        booklet += "*Программа будет объявлена позже*\n\n"

    # TODO: Можно удалить если не требуеться по заданию
    # Дополнительная информация
    booklet += "---\n"
    booklet += "*Место проведения:* Москва, ул. Пушкина, д. Колотушкина\n"
    booklet += "*Формат:* Офлайн + онлайн трансляция\n"
    booklet += "*Кофе-брейк:* предусмотрен\n\n"

    booklet += "Мы рады, что вы с нами!"

    return booklet

async def is_user_subscribed(user_id: int, event_id: int) -> bool:
    """Проверяет подписку (заглушка)"""
    is_subscribed = user_id in _subscriptions and event_id in \
                    _subscriptions[user_id]
    # TODO: УДАЛИТЬ принт
    print(
        f"Проверка подписки: пользователь {user_id} на мероприятие {event_id} = {is_subscribed}")
    return is_subscribed


async def get_event_subscribers(event_id: int) -> List[int]:
    """Получает подписчиков мероприятия (заглушка)"""
    subscribers = []
    for user_id, events in _subscriptions.items():
        if event_id in events:
            subscribers.append(user_id)
    # TODO: УДАЛИТЬ принт
    print(
        f"👥 Подписчики мероприятия {event_id}: {len(subscribers)} пользователей")
    return subscribers

# ШАБЛОН для будущего перехода на БД
"""
from asgiref.sync import sync_to_async
from meetup_core.models.Models import User, Event, EventSubscription
from datetime import datetime, timedelta

# TODO: УДАЛИТЬ заглушку _subscriptions при переходе на БД

@sync_to_async
def subscribe_to_event_db(user_id: int, event_id: int, bot=None) -> bool:
    try:
        user = User.objects.get(tg_id=user_id)
        event = Event.objects.get(id=event_id)
        subscription, created = EventSubscription.objects.get_or_create(
            user=user, event=event
        )
        
        if created and bot:
            await send_event_booklet_db(bot, user_id, event)
            
        return created
    except Exception as e:
        print(f"Ошибка подписки: {e}")
        return False

@sync_to_async 
def get_events_for_reminders():
    tomorrow = datetime.now().date() + timedelta(days=1)
    return list(Event.objects.filter(event_date=tomorrow))

@sync_to_async
def is_user_subscribed_db(user_id: int, event_id: int) -> bool:
    try:
        user = User.objects.get(tg_id=user_id)
        return EventSubscription.objects.filter(user=user, event_id=event_id).exists()
    except User.DoesNotExist:
        return False

@sync_to_async
def get_event_subscribers_db(event_id: int) -> List[int]:
    subscriptions = EventSubscription.objects.filter(event_id=event_id)
    return [sub.user.tg_id for sub in subscriptions]

async def send_event_booklet_db(bot, user_id: int, event):
    program = await sync_to_async(list)(event.speakertopic_set.all())
    
    booklet = "*ПРОГРАММА МЕРОПРИЯТИЯ*\n\n"
    
    if program:
        for i, session in enumerate(program, 1):
            booklet += f"{i}. *{session.topic}*\n"
            booklet += f"{session.started_at} - {session.ended_at}\n"
            booklet += f"Докладчик: {session.speaker.name}\n"
            booklet += "\n"
    else:
        booklet += "*Программа будет объявлена позже*\n\n"
    
    await bot.send_message(chat_id=user_id, text=booklet, parse_mode='Markdown')
"""