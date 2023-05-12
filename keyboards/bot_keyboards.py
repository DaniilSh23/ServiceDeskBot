from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from keyboards.bot_buttons import BUTTONS_DCT

ADMIN_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['ADMIN_PANEL']
    ],
    [
        BUTTONS_DCT['SEND_POST_TO_CHANNEL']
    ],
])

CANCEL_SEND_POST_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['CANCEL_SEND_TO_CHANNEL']
    ],
])

FOR_COPYED_POST_KBRD = InlineKeyboardMarkup([
    [
        BUTTONS_DCT['FOR_COPYED_POST_BTN']
    ],
])


async def form_webapp_kbrd(form_link, btn_text):
    """
    Формирование клавиатуры для перехода к форме, которая реализована через веб-приложение.
    :param form_link: ссылка на веб-форму.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=btn_text,
                web_app=WebAppInfo(url=form_link)
            )
        ],
    ])
