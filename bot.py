import os
from config.djando_config import setup_django
from telegram.ext import Application, CommandHandler
from ptb.handlers.conversation_handlers import conversation_handler


def main():
    setup_django()

    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not tg_bot_token:
        print("Токен не найден! Проверьте .env файл")
        exit()

    application = Application.builder().token(tg_bot_token).build()
    application.add_handler(conversation_handler)
    print("Бот запущен и слушает сообщения...")
    print("Отправьте /start в Telegram")

    application.run_polling()


if __name__ == '__main__':
    main()
