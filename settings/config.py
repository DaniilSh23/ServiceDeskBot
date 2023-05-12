import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN', '5265303938:AAE1daGp-VJR0R15J9tHksR38hQlbCXMYdU')
API_ID = os.environ.get('API_ID', '1234567890')
API_HASH = os.environ.get('API_HASH', 'какой-то там хэш')
FORM_LINK = os.environ.get('FORM_LINK', 'https://f5cc-78-30-211-223.ngrok-free.app/service_desk_bot/fill_an_app/')

# Константы для API Django проекта
BASE_HOST_URL = os.environ.get('BASE_HOST_URL', 'http://127.0.0.1:8000/')
CHECK_USER_URL = f'{BASE_HOST_URL}service_desk_bot/check_user/'

# Разные словари - хранилища бота
USER_STATES = dict()
