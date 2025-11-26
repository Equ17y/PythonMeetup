# Обработчик команд вида /команда
from ptb.keyboards import keyboard
from . import states_bot
from asgiref.sync import sync_to_async

async def guest_start(update, context):
    """
    Обработчик команды /start для гостя
    Регистрирует нового пользователя как гостя или найдет
    зарегистрированного
    """

    from meetup_core.models.Guest import Guest

    user = update.effective_user

    # Создание либо нахождения в базе данных записи гостя
    guest, created = await sync_to_async(Guest.objects.get_or_create)(
        telegram_id=user.id,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    )

    if created:
        message = f'''Добро пожаловать, {user.first_name}!
Вы успешно зарегистрированы как слушатель.

Используете кнопки ниже для навигации:'''
    else:
        message = f'''C возвращением, {guest.first_name}!

Используете кнопки ниже для навигации:'''

    await update.message.reply_text(
        text=message,
        reply_markup=keyboard.guest_keyboard(),
    )

    return states_bot.TEST
