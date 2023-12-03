import logging
import os

from urllib.parse import urlparse, parse_qs
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler

from core.places import get_nearby_places

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def show_nearby_paces(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_location = update.message.location
    # nearby_places = get_nearby_places(current_location, 100)
    nearby_places = [{'googleMapsUri': 'https://maps.google.com/?cid=12388013674260724962', 'displayName': {'text': 'LOTTE WORLD TOWER', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=6789200060716786287', 'displayName': {'text': 'Olympic Park', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=11928759293743347735', 'displayName': {'text': 'LOTTE WORLD AQUARIUM', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=249100100997713114', 'displayName': {'text': 'paradise walkerhill casino', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=11054188978324550532', 'displayName': {'text': 'Seoul Sky', 'languageCode': 'en'}},
                     {'googleMapsUri': 'https://maps.google.com/?cid=12195782186001824878', 'displayName': {'text': 'Seokchon Lake', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=5422997890015248632', 'displayName': {'text': 'Olympic Hall', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=13750433432067094988', 'displayName': {'text': 'Songpa Naru Park (Seokchon Lake Park)', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=8949511026676274477', 'displayName': {'text': 'LOTTE CINEMA World Tower', 'languageCode': 'en'}}, {'googleMapsUri': 'https://maps.google.com/?cid=18863179885171402', 'displayName': {'text': 'Jamsil stations', 'languageCode': 'en'}}]
    keyboard = [
        [create_inline_button_from_place(nearby_place)] for nearby_place in nearby_places
    ]
    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("더 알아보고 싶은 장소를 선택해주세요:", reply_markup=reply_markup)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="location set complete\n {} {}".format(current_location.latitude, current_location.longitude))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def guide_right_infront(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="guide right infront")


def create_inline_button_from_place(place):
    display_name = place.get('displayName').get('text')
    g_maps_cid = parse_qs(
        urlparse(place.get('googleMapsUri')).query).get('cid')[0]
    return InlineKeyboardButton(display_name, callback_data=f'{display_name}::{g_maps_cid}')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)
    application.add_handler(MessageHandler(
        filters.LOCATION, show_nearby_paces))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()
