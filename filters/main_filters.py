from pyrogram import filters

from settings.config import USER_STATES


async def ask_post_for_channel_func(_, __, query):
    """
    Фильтр для хэндлера ask_post_for_channel_handler
    """
    return query.data == 'send_post_to_channel'


async def send_post_to_channel_func(_, __, message):
    """
    Фильтр для хэндлера send_post_to_channel_handler.
    """
    if message.from_user:
        return USER_STATES.get(message.from_user.id, 'not_the_state') == 'ask_post_for_channel'


ask_post_for_channel_filter = filters.create(ask_post_for_channel_func)
send_post_to_channel_filter = filters.create(send_post_to_channel_func)
