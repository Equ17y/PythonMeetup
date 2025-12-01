from asgiref.sync import sync_to_async
from meetup_core.models import User, Event, EventSubscription
from datetime import datetime, timedelta
from typing import List
from telegram import Bot


@sync_to_async
def subscribe_to_all_events(user_id: int, bot=None) -> dict:
    try:
        user, created = User.objects.get_or_create(tg_id=user_id)

        # Получаем все предстоящие мероприятия
        next_events = Event.objects.filter(event_date__gte=datetime.now().date())

        if not next_events.exists():
            return {
                'success': True,
                'message': "На данный момент нет предстоящих мероприятий для подписки.",
            }

        subscribed_count = 0
        for event in next_events:
            subscription, created = EventSubscription.objects.get_or_create(
                user=user,
                event=event,
                defaults={'subscribed_at': datetime.now()}
            )
            if created:
                subscribed_count += 1

        if subscribed_count > 0:
            message = f"Вы успешно подписались на {subscribed_count} мероприятий!"
        else:
            message = "Вы уже подписаны на все предстоящие мероприятия."

        return {
            'success': True,
            'message': message,
        }

    except Exception as e:
        print(f"Ошибка при подписке: {e}")
        return {
            'success': False,
            'message': "Произошла ошибка при подписке. Попробуйте позже."
        }


async def notify_about_new_events(bot: Bot):
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
                await send_new_events_notification(bot, user.tg_id, events_list)
            except Exception:
                pass

    except Exception:
        pass


async def send_new_events_notification(bot, user_id: int, new_events: List):
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
