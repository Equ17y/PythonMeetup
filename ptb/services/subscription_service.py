from typing import List, Dict

# ВРЕМЕННО: заглушка вместо БД
_subscriptions: Dict[int, List[int]] = {}  # {user_id: [event_ids]}


async def subscribe_to_event(user_id: int, event_id: int) -> bool:
    """Подписывает пользователя на мероприятие (заглушка)"""
    print(f"🔔 Подписка: пользователь {user_id} на мероприятие {event_id}")

    if user_id not in _subscriptions:
        _subscriptions[user_id] = []

    if event_id not in _subscriptions[user_id]:
        _subscriptions[user_id].append(event_id)
        print(
            f"Пользователь {user_id} подписан на мероприятие {event_id}")
        return True

    print(
        f"Пользователь {user_id} уже подписан на мероприятие {event_id}")
    return False


async def is_user_subscribed(user_id: int, event_id: int) -> bool:
    """Проверяет подписку (заглушка)"""
    is_subscribed = user_id in _subscriptions and event_id in \
                    _subscriptions[user_id]
    print(
        f"🔍 Проверка подписки: пользователь {user_id} на мероприятие {event_id} = {is_subscribed}")
    return is_subscribed


async def get_event_subscribers(event_id: int) -> List[int]:
    """Получает подписчиков мероприятия (заглушка)"""
    subscribers = []
    for user_id, events in _subscriptions.items():
        if event_id in events:
            subscribers.append(user_id)

    print(
        f"👥 Подписчики мероприятия {event_id}: {len(subscribers)} пользователей")
    return subscribers


async def get_user_subscriptions(user_id: int) -> List[int]:
    """Получает мероприятия, на которые подписан пользователь"""
    return _subscriptions.get(user_id, [])


# ШАБЛОН для будущего перехода на БД
"""
# КОГДА БУДЕТ БД - раскомментировать:
from asgiref.sync import sync_to_async
from meetup_core.models.Models import User, Event, EventSubscription

@sync_to_async
def subscribe_to_event_db(user_id: int, event_id: int) -> bool:
    try:
        user = User.objects.get(tg_id=user_id)
        event = Event.objects.get(id=event_id)
        subscription, created = EventSubscription.objects.get_or_create(
            user=user, event=event
        )
        return created
    except Exception as e:
        print(f"Ошибка подписки: {e}")
        return False
"""
