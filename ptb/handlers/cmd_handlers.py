# Обработчик команд вида /команда
from ptb.keyboards import keyboard
from ptb.roles import get_user_role
from ptb.greeting_messages import get_welcome_message
from . import states_bot
from asgiref.sync import sync_to_async


async def start(update, context):
    """
    Обработчик команды /start для всех ролей
    """
    user = update.effective_user
    
    # Определяем роль пользователя
    role = get_user_role(user.id)

    # Получаем соответствующее приветственное сообщение
    welcome_message = get_welcome_message(role, user.first_name)
    
    # Получаем соответствующую клавиатуру
    if role == "speaker":
        reply_markup = keyboard.speaker_keyboard()
    elif role == "organizer":
        reply_markup = keyboard.organizer_keyboard()
    else:  # guest
        reply_markup = keyboard.guest_keyboard()

    await update.message.reply_text(
        text=welcome_message,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    return states_bot.MAIN_MENU

