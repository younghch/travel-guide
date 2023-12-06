import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler, CallbackQueryHandler

from core.places import get_nearby_places, get_names_of_place
from core.gpt import get_general_guide_of_places, get_detailed_guide_of_places_right_infront

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
ALLOWED_USER_NAME = os.environ.get('ALLOWED_USER_NAME')

GUIDE_MODE_KEY = 'guid_mode'
GPT_VERSION_KEY = 'gpt_version'
SELECT_PLACE_PREFIX = 'select_place'

GUIDE_MODE_RIGHT_INFRONT = 0
GUIDE_MODE_NEARBY_PLACES = 1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'gpt 여팽 가이드 입니다.\n' +
        '현재 위치를 공유하면 안내를 시작합니다.\n' +
        '가이드 방식을 선택하시려면 /mode를 입력해주세요.\n' +
        'gpt 버전을 선택하시려면 /gpt를 입력해주세요.\n' +
        '위치를 바꾸지 않고 안내를 받으려면 /guide를 입력해주세요.')


async def guide_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            '내 바로 앞 안내받기', callback_data=f'{GUIDE_MODE_KEY}{GUIDE_MODE_RIGHT_INFRONT}')],
        [InlineKeyboardButton(
            '주변 안내 받기', callback_data=f'{GUIDE_MODE_KEY}{GUIDE_MODE_NEARBY_PLACES}')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'안내 방법을 선택해주세요', reply_markup=reply_markup)


async def gpt_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            'gpt-3.5', callback_data=f'{GPT_VERSION_KEY}3')],
        [InlineKeyboardButton(
            'gpt-4', callback_data=f'{GPT_VERSION_KEY}4')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'gpt 버전을 선택해주세요', reply_markup=reply_markup)


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.from_user.username == ALLOWED_USER_NAME:
        await update.message.reply_text('현재는 허용된 사용자만 사용할 수 있습니다.')
        return
    guide_mode = context.user_data.get(
        GUIDE_MODE_KEY, GUIDE_MODE_RIGHT_INFRONT)
    gpt_version = context.user_data.get(GPT_VERSION_KEY, 3)
    if guide_mode == GUIDE_MODE_RIGHT_INFRONT:
        await guide_right_infront(update, context, gpt_version)
    elif guide_mode == GUIDE_MODE_NEARBY_PLACES:
        await show_nearby_places(update, context, gpt_version)


async def guide_right_infront(update: Update, context: ContextTypes.DEFAULT_TYPE, gpt_version):
    current_location = update.message.location
    nearby_places = []
    radius = 10
    while not nearby_places and radius < 200:
        nearby_places = get_nearby_places(current_location, radius)
        radius = radius * 1.8
    print(nearby_places)
    if not nearby_places:
        await update.message.reply_text('주변에 특별한 장소가 없습니다. 주변 안내 기능을 사용해보세요')
    else:
        await update.message.reply_text(
            get_detailed_guide_of_places_right_infront(
                list(map(get_names_of_place, nearby_places)),
                gpt_version)
        )


async def show_nearby_places(update: Update, context: ContextTypes.DEFAULT_TYPE, gpt_version):
    current_location = update.message.location
    nearby_places = []
    radius = 100
    while not nearby_places:
        nearby_places = get_nearby_places(current_location, radius)
        radius = radius * 2
    keyboard = [
        [create_inline_button_from_place(nearby_place, idx)] for idx, nearby_place in enumerate(nearby_places)
    ]
    context.user_data['nearby_places'] = nearby_places
    print(keyboard)
    reply_markup = InlineKeyboardMarkup(keyboard)
    place_overview = get_general_guide_of_places(
        list(map(get_names_of_place, nearby_places)), gpt_version)

    await update.message.reply_text(f'{place_overview}\n더 알아보고 싶은 장소를 선택해주세요:', reply_markup=reply_markup)


async def select_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    place_idx = int(query.data.split(SELECT_PLACE_PREFIX)[1])
    place = context.user_data.get('nearby_places')[place_idx]
    place_name = place.get('displayName').get('text')
    google_maps_url = place.get('googleMapsUri')

    await query.answer('답변을 생성중입니다.')
    detailed_guide = get_detailed_guide_of_places_right_infront([place_name])

    await query.edit_message_text(text=f'{detailed_guide}\n{google_maps_url}')


async def select_guide_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    guide_mode = int(query.data.split(GUIDE_MODE_KEY)[1])
    context.user_data[GUIDE_MODE_KEY] = guide_mode

    await query.answer()
    await query.edit_message_text(text=f'{"내 바로 앞 안내" if guide_mode == 0 else "주변 안내"}로 안내방식을 설정했습니다.')


async def select_gpt_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    gpt_version = int(query.data.split(GPT_VERSION_KEY)[1])
    context.user_data[GPT_VERSION_KEY] = gpt_version

    await query.answer()
    await query.edit_message_text(text=f'GPT-{gpt_version}을 사용합니다.')


def create_inline_button_from_place(place, id):
    display_name = place.get('displayName').get('text')
    return InlineKeyboardButton(display_name, callback_data=f'{SELECT_PLACE_PREFIX}{id}')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    start_handler = CommandHandler('start', start)
    guide_mode_handler = CommandHandler('mode', guide_mode)
    gpt_version_handler = CommandHandler('gpt', gpt_version)

    application.add_handler(start_handler)
    application.add_handler(guide_mode_handler)
    application.add_handler(gpt_version_handler)

    application.add_handler(MessageHandler(
        filters.LOCATION, location))

    application.add_handler(CallbackQueryHandler(
        select_place, pattern=f'^{SELECT_PLACE_PREFIX}'))
    application.add_handler(CallbackQueryHandler(
        select_guide_mode, pattern=f'^{GUIDE_MODE_KEY}'))
    application.add_handler(CallbackQueryHandler(
        select_gpt_type, pattern=f'^{GPT_VERSION_KEY}'))

    application.run_polling()
