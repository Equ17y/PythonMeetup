# Основные обработчики
from . import states_bot
from ptb.keyboards import keyboard
from ptb.roles import get_user_role
from asgiref.sync import sync_to_async


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
    
    # Общие обработчики для всех ролей
    if callback_data == 'program':
        await query.edit_message_text(
            "Программы мероприятий\n\nЗдесь будет список всех мероприятий...",
            reply_markup=get_role_keyboard(role)
        )
    
    elif callback_data == 'upcoming':
        await query.edit_message_text(
            "Предстоящие мероприятия\n\nЗдесь будет список предстоящих мероприятий...",
            reply_markup=get_role_keyboard(role)
        )
        
    # Обработчики для спикера
    elif callback_data == 'finish_speech':
        if role == "speaker":
            await query.edit_message_text(
                "Ваше выступление завершено! Спасибо за участие!",
                reply_markup=keyboard.speaker_keyboard()
            )
        else:
            await query.answer("Эта функция доступна только спикерам!", show_alert=True)
            
    # Обработчики для организатора
    elif callback_data == 'broadcast':
        if role == "organizer":
            await query.edit_message_text(
                "Программы мероприятий",
                reply_markup=keyboard.organizer_keyboard()
            )
        else:
            await query.answer("Эта функция доступна только организаторам!", show_alert=True)
    
    elif callback_data == 'broadcast':
        if role == "organizer":
            await query.edit_message_text(
                "Рассылка сообщений\n\nЗдесь будет интерфейс рассылки...",
                reply_markup=keyboard.organizer_keyboard()
            )
        else:
            await query.answer("Эта функция доступна только организаторам!", show_alert=True)

    return states_bot.MAIN_MENU

