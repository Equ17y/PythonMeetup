# Настройки для старта джанго
import os

import django
from dotenv import load_dotenv


def setup_django():
    load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetup.settings')
    django.setup()
    print('Django загружен')
