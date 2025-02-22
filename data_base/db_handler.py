from datetime import datetime

from data_base.connection import get_mysql_connection, get_mongo_connection


class DBHandler:
    def __init__(self):
        try:
            self.mysql_conn = get_mysql_connection()
            self.mysql_cursor = self.mysql_conn.cursor()
            print("Успешное подключение к MySQL.")
        except Exception as e:
            print("Ошибка подключения к MySQL:", e)
            self.mysql_conn = None

        try:
            self.mongo_client, self.mongo_collection = get_mongo_connection()
            print("Успешное подключение к MongoDB.")
        except Exception as e:
            print("Ошибка подключения к MongoDB:", e)
            self.mongo_client = None

    def search_by_keyword(self, keyword):
        query = """
            select f.title, f.description, f.release_year, c.name as genre
            from film f
            join film_category fc 
                on f.film_id = fc.film_id
            join category c 
                on fc.category_id = c.category_id
            where f.title like %s
            limit 10;
        """
        try:
            self.mysql_cursor.execute(query, (f"%{keyword}%",))
            return self.mysql_cursor.fetchall()
        except Exception as e:
            print("Ошибка запроса search_by_keyword:", e)
            return []

    def search_by_genre_year(self, genre, year):
        query = """
            select f.title, f.description, f.release_year, c.name as genre
            from film f
            join film_category fc 
                on f.film_id = fc.film_id
            join category c
                on fc.category_id = c.category_id
            where c.name = %s and f.release_year = %s
            limit 10
        """
        try:
            self.mysql_cursor.execute(query, (genre, year))
            return self.mysql_cursor.fetchall()
        except Exception as e:
            print("Ошибка запроса search_by_genre_year:", e)
            return []

    def search_year(self, year):
        query = """
            select f.title, f.description, f.release_year, c.name as genre
            from film f
            join film_category fc 
                on f.film_id = fc.film_id
            join category c 
                on fc.category_id = c.category_id
            where f.release_year = %s
            limit 10;
        """
        try:
            self.mysql_cursor.execute(query, (year,))
            return self.mysql_cursor.fetchall()
        except Exception as e:
            print("Ошибка запроса search_year:", e)
            return []

    def search_genre(self, genre):
        query = """
            select f.title, f.description, f.release_year, c.name as genre
            from film f
            join film_category fc 
                on f.film_id = fc.film_id
            join category c 
                on fc.category_id = c.category_id
            where c.name = %s
            limit 10;
        """
        try:
            self.mysql_cursor.execute(query, (genre,))
            return self.mysql_cursor.fetchall()
        except Exception as e:
            print("Ошибка запроса search_genre:", e)
            return []
    def get_years(self):
        query = """
            select distinct release_year
            from film
            order by release_year desc;
        """
        try:
            self.mysql_cursor.execute(query)
            results = self.mysql_cursor.fetchall()
            return [str(row["release_year"]) for row in results]
        except Exception as e:
            print("Ошибка получения годов:", e)
            return []

    def get_genres(self):
        query = """
            select distinct name
            from category
            order by name;
        """
        try:
            self.mysql_cursor.execute(query)
            results = self.mysql_cursor.fetchall()
            return [row['name'] for row in results]
        except Exception as e:
            print("Ошибка получения жанров:", e)
            return []

    def save_search_query(self, query_text, query_type):
        try:
            doc = {
                "query_text": query_text,
                "query_type": query_type,
                "timestamp": datetime.utcnow()
            }
            self.mongo_collection.insert_one(doc)
        except Exception as e:
            print("Ошибка сохранения запроса:", e)

    def get_popular_queries(self):
        try:
            pipeline = [
                {"$group": {"_id": "$query_type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10},
            ]
            return list(self.mongo_collection.aggregate(pipeline))
        except Exception as e:
            print("Ошибка получения популярных запросов:", e)
            return []

    def close_connection(self):
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.mongo_client:
            self.mongo_client.close()