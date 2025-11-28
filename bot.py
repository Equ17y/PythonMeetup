import os
import django
from dotenv import load_dotenv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetup.settings')
django.setup()

print("Django настроен")

from telegram.ext import Application
from ptb.handlers.conversation_handlers import conversation_handler

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print("Токен не найден! Проверьте .env файл")
    exit()


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(conversation_handler)
    print("Бот запущен и слушает сообщения...")
    print("Отправьте /start в Telegram")
    application.run_polling()


if __name__ == '__main__':
    main()
