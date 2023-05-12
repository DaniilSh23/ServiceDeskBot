from pyrogram.types import InlineKeyboardButton

from settings.config import BASE_HOST_URL, LINK_FOR_POST_BUTTON

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
    'FOR_COPYED_POST_BTN': InlineKeyboardButton(
        text=f'Оставить заявку',
        url=LINK_FOR_POST_BUTTON
    ),
}
