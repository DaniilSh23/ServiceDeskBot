from pyrogram.types import InlineKeyboardButton

from settings.config import BASE_HOST_URL

BUTTONS_DCT = {
    'ADMIN_PANEL': InlineKeyboardButton(
        text=f'⌨️Админ-панель',
        url=f'{BASE_HOST_URL}admin/'
    ),
    'SEND_POST_TO_CHANNEL': InlineKeyboardButton(
        text=f'🦔Отправить пост в канал',
        callback_data='send_post_to_channel'
    ),
    'CANCEL_SEND_TO_CHANNEL': InlineKeyboardButton(
        text=f'⛔️Остановить пересылку в канал',
        callback_data='cancel_send_post_to_channel'
    ),
}
