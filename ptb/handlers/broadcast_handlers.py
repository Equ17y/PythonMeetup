from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, filters
from . import states_bot
from ptb.keyboards import keyboard
from meetup_core.models.Models import User
from asgiref.sync import sync_to_async
from ptb.menu_utils import get_main_menu_message


@sync_to_async
def get_user_ids_by_role(role: str):
    """Получение ID по ролям из БД"""
    users = User.objects.filter(user_role=role)
    return [user.tg_id for user in users]


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало процесса рассылки через callback"""
    query = update.callback_query
    await query.answer()

    # Сообщение с инструкцией
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Массовая рассылка \n\nВведите текст для рассылки:",
        reply_markup=ReplyKeyboardRemove()
    )

    return states_bot.BROADCAST_TEXT


async def receive_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем текст рассылки"""
    context.user_data['broadcast_text'] = update.message.text

    user_ids = await get_user_ids_by_role('guest')

    await update.message.reply_text(
        f"Ваша рассылка готова:\n\n{update.message.text}\n\n"
        f"Получателей: {len(user_ids)}\n\nПодтвердите отправку:",
        parse_mode='Markdown',
        reply_markup=keyboard.broadcast_confirmation_keyboard()
    )

    return states_bot.BROADCAST_CONFIRM


async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение рассылки"""
    if "Отменить" in update.message.text:
        await update.message.reply_text(
            "Рассылка отменена",
            reply_markup=ReplyKeyboardRemove()
        )
        # Возвращаем клавиатуру организатора
        message_text, reply_markup = await get_main_menu_message(
            update.effective_user.id, update.effective_user.first_name
        )

        await update.message.reply_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        context.user_data.clear()
        return states_bot.MAIN_MENU

    # Получаем текст
    text = context.user_data.get('broadcast_text', '')
    user_ids = await get_user_ids_by_role('guest')

    # Тест без реальной отправки
    await update.message.reply_text(
        f"Тест рассылки завершен!\n\n"
        f"Текст: {text}\n"
        f"Получили бы: *{len(user_ids)}* пользователей\n\n"
        f"С БД сообщения будут отправлены всем участникам.",
        parse_mode='Markdown',
        reply_markup=ReplyKeyboardRemove()
    )

    # Возвращаем клавиатуру организатора
    message_text, reply_markup = await get_main_menu_message(
        update.effective_user.id, update.effective_user.first_name
    )

    await update.message.reply_text(
        text=message_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

    context.user_data.clear()
    return states_bot.MAIN_MENU
