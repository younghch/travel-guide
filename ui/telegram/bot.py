import logging
import os
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def location(update:Update, context: ContextTypes.DEFAULT_TYPE):
    current_location = update.message.location
    context.user_data['current_location'] = current_location
    print(current_location)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="your location is {} {}".format(current_location.latitude, current_location.longitude))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    
    start_handler = CommandHandler('start', start)
    location_handler = CommandHandler('location', location)

    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.LOCATION, location))

    application.run_polling()