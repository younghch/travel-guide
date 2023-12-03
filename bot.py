import logging
import os

from urllib.parse import urlparse, parse_qs
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler

from core.places import get_nearby_places
from core.gpt import get_general_guide_of_places, get_detailed_guide_of_a_place

QUERY_SEPARATOR = '::'
GOOGLE_MAPS_PREFIX = 'https://maps.google.com/?cid='

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='안내를 받으려면 현재 위치를 보내주세요.')


async def show_nearby_places(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_location = update.message.location
    nearby_places = []
    radius = 100
    while not nearby_places:
        nearby_places = get_nearby_places(current_location, radius)
        radius = radius * 2
    keyboard = [
        [create_inline_button_from_place(nearby_place)] for nearby_place in nearby_places
    ]
    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    place_overview = get_general_guide_of_places(
        list(map(lambda place: place.get('displayName').get('text'), nearby_places)))

    await update.message.reply_text(f'{place_overview}\n더 알아보고 싶은 장소를 선택해주세요:', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    [place_name, google_cid] = query.data.split(QUERY_SEPARATOR)

    google_maps_url = f'{GOOGLE_MAPS_PREFIX}{google_cid}'
    await query.answer('답변을 생성중입니다.')
    detailed_guide = get_detailed_guide_of_a_place(place_name)

    await query.edit_message_text(text=f'{detailed_guide}\n{google_maps_url}')


async def guide_right_infront(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='guide right infront')


def create_inline_button_from_place(place):
    display_name = place.get('displayName').get('text')
    g_maps_cid = parse_qs(
        urlparse(place.get('googleMapsUri')).query).get('cid')[0]
    return InlineKeyboardButton(display_name, callback_data=f'{display_name}{QUERY_SEPARATOR}{g_maps_cid}')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(MessageHandler(
        filters.LOCATION, show_nearby_places))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
