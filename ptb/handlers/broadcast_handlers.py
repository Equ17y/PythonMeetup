from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from . import states_bot
from ptb.keyboards import keyboard
from meetup_core.models import User
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
    await query.edit_message_text(
        text="*Массовая рассылка*\n\nВведите текст для рассылки:",
        parse_mode='Markdown',
        reply_markup=None
    )

    return states_bot.BROADCAST_TEXT


async def receive_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получаем текст рассылки"""
    broadcast_text = update.message.text
    context.user_data['broadcast_text'] = broadcast_text

    # Получаем всех пользователей с ролью гостя
    user_ids = await get_user_ids_by_role('guest')

    await update.message.reply_text(
        f"*Ваша рассылка готова:*\n\n{broadcast_text}\n\n"
        f"*Получателей (гости):* {len(user_ids)}\n\n"
        f"*Подтвердите отправку:*",
        parse_mode='Markdown',
        reply_markup=keyboard.broadcast_confirmation_keyboard()
    )

    return states_bot.BROADCAST_CONFIRM


async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Подтверждение рассылки"""
    user_input = update.message.text
    broadcast_text = context.user_data.get('broadcast_text', '')

    if user_input == "Отменить":
        await update.message.reply_text(
            "*Рассылка отменена*",
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

    elif user_input == "Разослать":
        user_ids = await get_user_ids_by_role('guest')

        # Отправляем сообщение всем пользователям с ролью гостя
        sent_count = 0
        failed_count = 0

        # Уведомление о начале рассылки
        progress_msg = await update.message.reply_text(
            "*Начинаю рассылку...*",
            parse_mode='Markdown'
        )

        for user_id in user_ids:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"*Рассылка от организатора:*\n\n{broadcast_text}",
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
                failed_count += 1

        # Обновляем сообщение о прогрессе
        await progress_msg.edit_text(
            f"*Рассылка завершена!*\n\n"
            f"*Статистика:*\n"
            f"• Успешно отправлено: *{sent_count}*\n"
            f"• Не удалось отправить: *{failed_count}*\n"
            f"• Всего получателей: *{len(user_ids)}*",
            parse_mode='Markdown'
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

    # Если введен неправильный ответ
    await update.message.reply_text(
        "*Неверный выбор.* Используйте кнопки ниже:",
        reply_markup=keyboard.broadcast_confirmation_keyboard(),
        parse_mode='Markdown'
    )
    return states_bot.BROADCAST_CONFIRM
