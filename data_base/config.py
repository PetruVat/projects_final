import os
import dotenv
from pymysql.cursors import DictCursor


dotenv.load_dotenv()

MYSQL_CONFIG = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'db': os.getenv('DATABASE'),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

MONGO_CONFIG = {
    'host': os.getenv('MONGO_HOST'),
    'port': int(os.getenv('MONGO_PORT')),
    'db_name': os.getenv('MONGO_DB'),
    'collection_name': os.getenv('MONGO_COLLECTION')
}