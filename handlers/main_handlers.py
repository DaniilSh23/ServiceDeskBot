from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from filters.main_filters import new_comment_filter, answer_comment_filter, cancel_comment_answer_filter, \
    send_comment_answer_filter
from keyboards.bot_keyboards import form_webapp_kbrd, new_comment_kbrd, CANCEL_SEND_COMMENT_KBRD
from secondary_functions.req_to_bot_api import post_for_check_user
from settings.config import FORM_LINK, ANSWER_COMMENT_STATES


@Client.on_message(filters.command(['start', 'menu']))
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
            text=f'К сожалению, у Вас нет доступа к дальнейшему функционалу. Вы точно сотрудник ЦФУ? 💼\n'
                 f'Также, пожалуйста, проверьте, что у Вас указан username в профиле Telegram 🪪'
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


@Client.on_message(filters.me & filters.private & new_comment_filter)
async def new_comment_handler(client, update: Message):
    """
    Хэндлер для получения нового коммента и изменения его
    """
    _, task_id, task_title, comment_text = update.text.split('---')
    await update.edit_text(
        text=f'🆕 <b>Новый комментарий по Вашей заявке</b>: {task_title}\n\n'
             f'<i>{comment_text}</i>',
        reply_markup=await new_comment_kbrd(task_id=task_id),
    )


@Client.on_callback_query(answer_comment_filter)
async def answer_comment_handler(client, update: CallbackQuery):
    """
    Хэндлер для нажатия на кнопку ответа на коммент
    """
    ANSWER_COMMENT_STATES[update.from_user.id] = f'input_comment {update.data.split()[1]} {update.message.id}'
    await update.answer(f'Пришлите боту ответ.')
    await update.edit_message_text(
        text=f'{update.message.text}\n\n==========\n‼️ <b>Пришлите ответным сообщением текст Вашего комментария.</b>',
        reply_markup=CANCEL_SEND_COMMENT_KBRD
    )


@Client.on_callback_query(cancel_comment_answer_filter)
async def cancel_comment_answer_handler(client, update: CallbackQuery):
    """
    Хэндлер для нажатия на кнопку отмены при вводе ответа на коммент.
    """
    await update.answer(f'Отмена ответа на комментарий.')
    task_id = ANSWER_COMMENT_STATES[update.from_user.id].split()[1]
    await update.edit_message_text(
        text=f'{update.message.text.split("==========")[0]}',
        reply_markup=await new_comment_kbrd(task_id=task_id)
    )
    ANSWER_COMMENT_STATES.pop(update.from_user.id)


@Client.on_message(filters.private & send_comment_answer_filter)
async def send_comment_answer(client, update: Message):
    """
    Хэндлер для отправки ответа на коммент в Битру.
    """
    task_id = ANSWER_COMMENT_STATES[update.from_user.id].split()[1]
    msg_id = ANSWER_COMMENT_STATES[update.from_user.id].split()[2]
    info_msg = await update.reply_text(text='📡 <b>Отправляю Ваш ответ в Битрикс...</b>')

    # TODO: дописать отправку коммента в битру, через веб-приложение

    comment_msg = await client.get_messages(
        chat_id=update.from_user.id,
        message_ids=int(msg_id),
    )
    await comment_msg.edit_text(
        text=f'{comment_msg.text.split("==========")[0]}👌 <b>Ваш ответ: </b>{update.text}'
    )
