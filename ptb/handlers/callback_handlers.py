# Основные обработчики
from . import states_bot
from ptb.keyboards import keyboard
from ptb.keyboards.program_keyboard import (
    events_list_keyboard, event_program_keyboard
)
from ptb.keyboards.next_events_keyboard import (
    next_events_list_keyboard,
    next_event_program_keyboard
)
from ptb.events_data import (
    get_today_events, get_event_program,
    get_next_events, get_next_event_program,
)
from ptb.roles import get_user_role
from .broadcast_handlers import start_broadcast
from ptb.menu_utils import get_main_menu_message
from ptb.services.subscription_service import subscribe_to_all_events, is_user_subscribed
from asgiref.sync import sync_to_async


async def safe_edit_message(query, new_text, reply_markup=None, parse_mode=None):
    """
    Безопасная замена текста сообщения
    """
    current_text = query.message.text_html or query.message.text

    if current_text == new_text:
        try:
            await query.edit_message_reply_markup(reply_markup=reply_markup)
        except Exception:
            pass
        return

    await query.edit_message_text(
        new_text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )


def get_role_keyboard(role):
    """
    Возвращает клавиатуру в зависимости от роли
    """
    if role == "speaker":
        return keyboard.speaker_keyboard()
    elif role == "organizer":
        return keyboard.organizer_keyboard()
    else:
        return keyboard.guest_keyboard()


async def main_menu_handler(update, context):
    """
    Обработчик callback'ов для главного меню всех ролей
    """

    query = update.callback_query
    await query.answer()

    callback_data = query.data
    user = query.from_user

    role = await sync_to_async(get_user_role)(user.id, user.username)

    if callback_data == 'program':
        events = await sync_to_async(get_today_events)()
        message_text = format_events_list_message(events)

        await safe_edit_message(
            query,
            message_text,
            reply_markup=events_list_keyboard(events),
            parse_mode='Markdown'
        )
        return states_bot.EVENTS_LIST

    elif callback_data == 'quick_subscribe':
        user_id = query.from_user.id
        result = await subscribe_to_all_events(user_id, context.bot)

        await safe_edit_message(
            query,
            result['message'],
            reply_markup=get_role_keyboard(role),
            parse_mode='Markdown'
        )
        return states_bot.MAIN_MENU

    elif callback_data == 'upcoming':
        next_events = await sync_to_async(get_next_events)()

        message_text = format_next_events_message(next_events)

        await safe_edit_message(
            query,
            message_text,
            reply_markup=next_events_list_keyboard(next_events),
            parse_mode='Markdown'
        )
        return states_bot.NEXT_EVENTS_LIST

    elif callback_data == 'event_programs':
        if role == "organizer":
            events = await sync_to_async(get_today_events)()
            message_text = format_events_list_message(events)

            await query.edit_message_text(
                message_text,
                reply_markup=events_list_keyboard(events),
                parse_mode='Markdown'
            )
            return states_bot.EVENTS_LIST
        else:
            await query.answer("Эта функция доступна только организаторам!",
                               show_alert=True)

    elif callback_data == 'broadcast':
        if role == "organizer":
            return await start_broadcast(update, context)
        else:
            await query.answer("Эта функция доступна только организаторам!", show_alert=True)

    return states_bot.MAIN_MENU


async def events_list_handler(update, context):
    """
    Обработчик для списка мероприятий
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data.startswith('event_'):
        event_id = int(callback_data.split('_')[1])
        events = await sync_to_async(get_today_events)()
        event = next((e for e in events if e['id'] == event_id), None)

        if event:
            program = await sync_to_async(get_event_program)(event_id)

            message_text = format_event_program_message(event, program)

            await safe_edit_message(
                query,
                message_text,
                reply_markup=event_program_keyboard(event_id),
                parse_mode='Markdown'
            )
            return states_bot.EVENT_PROGRAM

    elif callback_data == 'back_to_main':
        message_text, reply_markup = await get_main_menu_message(
            query.from_user.id,
            query.from_user.first_name
        )
        await safe_edit_message(
            query,
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return states_bot.MAIN_MENU

    elif callback_data == 'back_to_events':
        events = await sync_to_async(get_today_events)()

        message_text = format_events_list_message(events)

        await safe_edit_message(
            query,
            message_text,
            reply_markup=events_list_keyboard(events),
            parse_mode='Markdown'
        )
        return states_bot.EVENTS_LIST

    return states_bot.EVENTS_LIST


async def next_events_list_handler(update, context):
    """
    Обработчик для списка предстоящих мероприятий
    """
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    user_id = query.from_user.id

    if callback_data.startswith('event_'):
        event_id = int(callback_data.split('_')[1])
        events = await sync_to_async(get_next_events)()
        event = next((e for e in events if e['id'] == event_id), None)

        if event:
            subscribed = await is_user_subscribed(user_id, event_id)
            program = await sync_to_async(get_next_event_program)(event_id)

            message_text = format_next_event_program_message(event, program)

            await safe_edit_message(
                query,
                message_text,
                reply_markup=next_event_program_keyboard(event_id),
                parse_mode='Markdown'
            )
            return states_bot.NEXT_EVENT_PROGRAM

    elif callback_data.startswith("subscribe_"):
        event_id = int(callback_data.split("_")[1])
        user_id = query.from_user.id

        events = await sync_to_async(get_next_events)()
        event = next((e for e in events if e["id"] == event_id), None)

        if event:
            success = await subscribe_to_event(user_id, event_id)

            if success:
                event_name = event["name"]
                event_date = event["event_date"].strftime("%d.%m.%Y")
                event_time = f"{event['started_at'].strftime('%H:%M')} – {event['ended_at'].strftime('%H:%M')}"

                text = (
                    f"🎉 *Вы подписались на мероприятие!*\n\n"
                    f"*{event_name}*\n"
                    f"📅 {event_date}\n"
                    f"⏰ {event_time}\n\n"
                    f"Вам придет напоминание за день до начала мероприятия."
                )

                await query.edit_message_text(
                    text,
                    reply_markup=next_event_program_keyboard(event_id, subscribed=True),
                    parse_mode="Markdown"
                )

            else:
                await query.answer("Вы уже подписаны на это мероприятие!",show_alert=True)
        else:
            await query.answer("Ошибка: мероприятие не найдено.", show_alert=True)

        return states_bot.NEXT_EVENT_PROGRAM

    elif callback_data == 'back_to_main':
        message_text, reply_markup = await get_main_menu_message(
            query.from_user.id,
            query.from_user.first_name
        )
        await safe_edit_message(
            query,
            message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return states_bot.MAIN_MENU

    elif callback_data == 'back_to_events':
        events = await sync_to_async(get_next_events)()

        message_text = format_next_events_message(events)

        await safe_edit_message(
            query,
            message_text,
            reply_markup=next_events_list_keyboard(events),
            parse_mode='Markdown'
        )
        return states_bot.NEXT_EVENTS_LIST

    return states_bot.NEXT_EVENTS_LIST


def format_events_list_message(events):
    """
    Форматирует сообщение со списком мероприятий
    """
    if not events:
        return "На сегодня мероприятий нет."

    message = "*Мероприятия на сегодня:*\n\n"

    for event in events:
        time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"
        status = " 🟢 *ИДЕТ СЕЙЧАС*" if event['is_active'] else ""

        message += f"• *{event['name']}*\n"
        message += f"  🕐 {time_str}{status}\n\n"

    message += "Выберите мероприятие, чтобы увидеть подробную программу.\n\n"

    return message


def format_event_program_message(event, program):
    """
    Форматирует сообщение с программой мероприятия
    """
    date_str = event['event_date'].strftime('%d.%m.%y')
    time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"

    message = f"*{event['name']}*\n"
    message += f"{date_str} • {time_str}\n\n"

    if program:
        message += "*Программа:*\n\n"
        for session in program:
            status = " 🟢 *ИДЕТ СЕЙЧАС*" if session['is_active'] else ""
            finished = " ✓" if session['is_finished'] else ""

            speaker_link = (
                f"[{session['speaker']}](https://t.me/{session['speaker_username'][1:]})"
                if session['speaker_username']
                else session['speaker']
            )

            message += f"{session['topic']}{finished}\n"
            message += f"{session['started_at']} - {session['ended_at']} {status}\n"
            message += f"Докладчик: {speaker_link}\n\n"
    else:
        message += "Программа мероприятия пока не доступна.\n"

    return message


def format_next_events_message(events):
    """
    Форматирует сообщение со списком следующих мероприятий
    """
    if not events:
        return "Предстоящих мероприятия нет."

    message = "*Предстоящие мероприятия:*\n\n"

    for event in events:
        time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"

        message += f"• *{event['name']}*\n"
        message += f"{event['event_date'].strftime('%d.%m.%Y')}  🕐 {time_str}\n\n"

    message += "Выберите мероприятие, чтобы увидеть подробную программу, и подписаться.\n\n"

    return message


def format_next_event_program_message(event, program):
    """
    Форматирует сообщение с программой мероприятия
    """
    date_str = event['event_date'].strftime('%d.%m.%y')
    time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"

    message = f"*{event['name']}*\n"
    message += f"{date_str} • {time_str}\n\n"

    if program:
        message += "*Программа:*\n\n"
        for session in program:
            message += f"{session['topic']}\n"
            message += f"{session['started_at']} - {session['ended_at']}\n"
            message += f"Докладчик: {session['speaker']}\n\n"
    else:
        message += "Программа мероприятия пока не доступна.\n"

    return message
