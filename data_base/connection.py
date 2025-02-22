import pymysql
from pymongo import MongoClient
from data_base.config import MYSQL_CONFIG, MONGO_CONFIG

def get_mysql_connection():
    return pymysql.connect(**MYSQL_CONFIG)

def get_mongo_connection():
    client = MongoClient(MONGO_CONFIG['host'], MONGO_CONFIG['port'])
    db = client[MONGO_CONFIG['db_name']]
    return client, db[MONGO_CONFIG['collection_name']]