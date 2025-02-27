import os
import dotenv
import pymysql
from pymysql.cursors import DictCursor

# Загружает переменные окружения из .env.
dotenv.load_dotenv()

# Настраивает параметры для подключения к MySQL.
MYSQL_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'db': os.getenv('DATABASE'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Настраивает параметры для подключения к MongoDB.
MONGO_CONFIG = {
    'host': os.getenv('MONGO_HOST'),
    'port': int(os.getenv('MONGO_PORT')),
    'db_name': os.getenv('MONGO_DB'),
    'collection_name': os.getenv('MONGO_COLLECTION')
}

# Безопасность (пароли не хранятся в коде).
# Гибкость (можно менять параметры без изменения кода).
# Удобство (код становится чище и легче для поддержки).