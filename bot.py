import os
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update, context):
    await update.message.reply_text('Приветствую тебя пользователь!')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Бот запущен и слушает сообщения...")
    application.run_polling()

if __name__ == '__main__':
    main()