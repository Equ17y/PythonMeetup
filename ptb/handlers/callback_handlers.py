# Основные обработчики
from . import states_bot
from ptb.keyboards import keyboard
from ptb.keyboards.program_keyboard import events_list_keyboard, event_program_keyboard
from ptb.events_data import get_today_events, get_event_program, finish_current_talk_for_speaker
from ptb.roles import get_user_role
from asgiref.sync import sync_to_async
from datetime import datetime
from .broadcast_handlers import start_broadcast, receive_broadcast_text, confirm_broadcast

from ptb.menu_utils import get_main_menu_message


async def safe_edit_message(query, new_text, reply_markup=None, parse_mode=None):
    """
    Безопасная замена текста сообщения:
    - обновляет только если текст реально изменился
    - предотвращает ошибку "Message is not modified"
    """
    current_text = query.message.text_html or query.message.text

    if current_text == new_text:
        # Сообщение такое же — просто заменяем клавиатуру, если она отличается
        try:
            await query.edit_message_reply_markup(reply_markup=reply_markup)
        except Exception:
            pass
        return

    # Если текст другой — спокойно обновляем
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
    role = get_user_role(user.id)
    
    # Обработка программы мероприятий
    if callback_data == 'program':
        events = get_today_events()
        
        # Формируем подробное сообщение со списком мероприятий
        message_text = format_events_list_message(events)
        
        await safe_edit_message(
            query,
            message_text,
            reply_markup=events_list_keyboard(events),
            parse_mode='Markdown'
        )
        return states_bot.EVENTS_LIST
    
    # Обработка предстоящих мероприятий
    elif callback_data == 'upcoming':
        await safe_edit_message(
            query,
            "Предстоящие мероприятия\n\nЗдесь будет список предстоящих мероприятий...",
            reply_markup=get_role_keyboard(role)
        )
        
    # Обработчики для спикера
    elif callback_data == 'finish_speech':
        if role == "speaker":
            user = query.from_user
            username = user.username

            if not username:
                await query.answer(
                    "У вашего Telegram-профиля не задан username",
                    show_alert=True
                )
                return states_bot.MAIN_MENU

            event, session = finish_current_talk_for_speaker(username)

            if event and session:
                text = (
                    f"Вы завершили свое выступление!\n\n"
                    f"Мероприятие: *{event['name']}*\n"
                    f"Доклад: *{session['topic']}*\n\n"
                    f"Спасибо за участие!"
                )
                await safe_edit_message(
                    query,
                    text,
                    reply_markup=keyboard.speaker_keyboard(),
                    parse_mode='Markdown'
                )
            else:
                await query.answer(
                    "Сейчас нет активного доклада, привязанного к вашему аккаунту.\n"
                    "Возможно, ваш доклад ещё не начался или уже завершён.",
                    show_alert=True
                )
        else:
            await query.answer("Эта функция доступна только спикерам!", show_alert=True)
            
    # Обработчики для организатора
    elif callback_data == 'event_programs':
        if role == "organizer":
            events = get_today_events()
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

    elif callback_data == 'broadcast':  # Второй обработчик - для рассылки
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
    
    # Обработка выбора конкретного мероприятия
    if callback_data.startswith('event_'):
        event_id = int(callback_data.split('_')[1])
        events = get_today_events()
        event = next((e for e in events if e['id'] == event_id), None)
        
        if event:
            # Получаем программу мероприятия
            program = get_event_program(event_id)
            
            # Формируем сообщение с программой
            message_text = format_event_program_message(event, program)
            
            await safe_edit_message(
                query,
                message_text,
                reply_markup=event_program_keyboard(event_id),
                parse_mode='Markdown'
            )
            return states_bot.EVENT_PROGRAM
        
    # Обработка кнопки "Назад" в главное меню
    elif callback_data == 'back_to_main':
        # Используем функцию из утилит
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
    
    # Обработка кнопки "Назад" к списку мероприятий
    elif callback_data == 'back_to_events':
        events = get_today_events()
        
        message_text = format_events_list_message(events)
        
        await safe_edit_message(
            query,
            message_text,
            reply_markup=events_list_keyboard(events),
            parse_mode='Markdown'
        )
        return states_bot.EVENTS_LIST
    
    return states_bot.EVENTS_LIST


def format_events_list_message(events):
    """
    Форматирует сообщение со списком мероприятий
    """
    if not events:
        return "На сегодня мероприятий нет."
    
    message = "*Мероприятия на сегодня:*\n\n"
    
    for event in events:
        # Форматируем время
        time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"
        
        # Добавляем статус "Идет сейчас"
        status = " 🟢 *ИДЕТ СЕЙЧАС*" if event['is_active'] else ""
        
        message += f"• *{event['name']}*\n"
        message += f"  🕐 {time_str}{status}\n\n"
        
    message += "Выберите мероприятие, чтобы увидеть подробную программу.\n\n"
    
    return message


def format_event_program_message(event, program):
    """
    Форматирует сообщение с программой мероприятия
    """
    # Заголовок мероприятия
    date_str = event['event_date'].strftime('%d.%m.%y')
    time_str = f"{event['started_at'].strftime('%H:%M')} - {event['ended_at'].strftime('%H:%M')}"
    
    message = f"*{event['name']}*\n"
    message += f"{date_str} • {time_str}\n\n"
    
    # Программа
    if program:
        message += "*Программа:*\n\n"
        for session in program:
            status = " 🟢 *ИДЕТ СЕЙЧАС*" if session['is_active'] else ""
            clean_username = session['speaker_username'].lstrip("@")
            speaker_link = (
                    f"[{session['speaker']}](https://t.me/{session['speaker_username'][1:]})"
                    if session['speaker_username']
                    else session['speaker']
                )
            message += f"{session['topic']}\n"
            message += f"{session['started_at']} - {session['ended_at']} {status}\n"
            message += f"Докладчик: {speaker_link}\n\n"
    else:
        message += "Программа мероприятия пока не доступна.\n"
    
    return message

