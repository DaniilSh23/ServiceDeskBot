from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message

from filters.main_filters import ask_post_for_channel_filter, send_post_to_channel_filter
from keyboards.bot_keyboards import form_webapp_kbrd, ADMIN_KBRD, CANCEL_SEND_POST_KBRD, FOR_COPYED_POST_KBRD
from secondary_functions.req_to_bot_api import post_for_check_user
from settings.config import FORM_LINK, USER_STATES, CHANNEL_ID


@Client.on_message(filters.command(['start']))
async def start_handler(client, update):
    """
    Совершаем проверку наличия и активности юзера в Битриксе,
    если проверка дала положительный результат, то отдаём кнопку на форму для оставления заявки в Service Desk.
    """
    check_usr_rslt = await post_for_check_user(tlg_username=update.from_user.username, tlg_id=update.from_user.id)

    if check_usr_rslt == 200:
        await update.reply_text(
            text='Подайте новую заявку в тех.поддержку, нажав на кнопку ниже.👇',
            reply_markup=await form_webapp_kbrd(form_link=FORM_LINK, btn_text='🖊Подать заявку')
        )

    elif check_usr_rslt == 400:
        await update.reply_text(
            text=f'Неудачная проверка доступа. Возможно у Вас не указан username в профиле Telegram 🪪'
        )

    elif check_usr_rslt == 403:
        await update.reply_text(
            text=f'К сожалению, у Вас нет доступа к дальнейшему функционалу. Вы точно сотрудник ЦФУ? 💼'
        )

    elif check_usr_rslt == 502:
        await update.reply_text(
            text=f'Не удалось до конца провести проверку доступа. Проблема во взаимодействии с Битрикс. 🚧'
        )

    else:
        await update.reply_text(
            text=f'🔮 Произошло что-то непредвиденное...какая-то тёмная магия...\n'
                 f'Даже боюсь представить что, но бот не может дальше продолжать работать.'
        )




# TODO: ниже хэндлеры с прошлого проекта, позже можно будет удалить
@Client.on_callback_query(ask_post_for_channel_filter)
async def ask_post_for_channel_handler(client, update: CallbackQuery):
    """
    Запрашиваем пост для отправки его в канал.
    """
    await update.edit_message_text(
        text=f'Окей. Пришлите мне пост. (всё, что сейчас отправите, я перешлю в канал, поэтому будьте внимательны!)'
             f'Если вы закончили, то нажмите кнопку ниже.',
        reply_markup=CANCEL_SEND_POST_KBRD
    )
    USER_STATES[update.from_user.id] = 'ask_post_for_channel'


@Client.on_message(send_post_to_channel_filter)
async def send_post_to_channel_handler(client, update: Message):
    """
    Пересылаем пост в канал
    """
    try:
        forwarded_message = await update.copy(
            chat_id=CHANNEL_ID,
            reply_markup=FOR_COPYED_POST_KBRD
        )
    except Exception as error:
        await update.reply_text(
            text=f'❌Пост не отправлен. Текст ошибки:\n\n{error}'
        )
        return

    await update.reply_text(
        text=f'✅Пост отправлен\n\n'
             f'Ссылка на пост:https://t.me/{forwarded_message.sender_chat.username}/{forwarded_message.id}',
        reply_markup=CANCEL_SEND_POST_KBRD
    )


@Client.on_callback_query()
async def cancel_send_post_to_channel_handler(client, update: CallbackQuery):
    """
    Хэндлер для отмены пересылки постов в канал.
    """
    USER_STATES.pop(update.from_user.id)    # Очищаем стэйт
    await update.edit_message_text(
        text=f'👑Меню админа',
        reply_markup=ADMIN_KBRD,
    )


# @Client.on_message(filters.channel | filters.all)
# async def update_echo(client, update):
#     # print(update)
#     print(CHANNEL_ID)
