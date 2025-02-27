from datetime import datetime

from data_base.connection import get_mysql_connection, get_mongo_connection


class DBHandler:
    """Класс для работы с базами данных MySQL и MongoDB."""
    def __init__(self):
        """Инициализация соединений с MySQL и MongoDB."""
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
        """Поиск фильмов по ключевому слову в названии или описании."""
        query = """
            select f.title, f.description, f.release_year, c.name as genre
            from film f
            join film_category fc 
                on f.film_id = fc.film_id
            join category c 
                on fc.category_id = c.category_id
            where f.title like %s
            or description like %s
            limit 10;
        """
        try:
            self.mysql_cursor.execute(query, (f"%{keyword}%", f"%{keyword}%",))
            return self.mysql_cursor.fetchall()
        except Exception as e:
            print("Ошибка запроса search_by_keyword:", e)
            return []

    def search_by_genre_year(self, genre, year):
        """Поиск фильмов по жанру и году."""
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
        """Поиск фильмов по году выпуска."""
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
        """Поиск фильмов по жанру."""
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
        """Получение списка доступных лет выпуска фильмов."""
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
        """Получение списка доступных жанров фильмов."""
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

    # ========= Сохранение в MongoDB =================================================================================
    def save_search_query(self, query_text, query_type):
        """Сохранение поискового запроса в MongoDB."""
        if self.mongo_collection is None:
            return
        try:
            doc = {
                "query_text": query_text,
                "query_type": query_type,
                "timestamp": datetime.utcnow()
            }
            self.mongo_collection.insert_one(doc)
        except Exception as e:
            print("Ошибка сохранения запроса:", e)

    def get_top_keywords_mongo(self, limit=10):
        """Получение топ-10 самых популярных запросов по названию или описанию из MongoDB."""
        if self.mongo_collection is None:
            return []
        try:
            pipeline = [
                {"$match": {"query_type": "search_keyword"}},
                {"$group": {"_id": "$query_text", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]
            return list(self.mongo_collection.aggregate(pipeline))
        except Exception as e:
            print("Ошибка получения топ-ключевых слов:", e)
            return []

    def get_top_genres_years_mongo(self, limit=10):
        """Получение топ-10 самых популярных запросов по жанру и году из MongoDB."""
        if self.mongo_collection is None:
            return []
        try:
            pipeline = [
                {"$match": {"query_type": "search_genre_year"}},
                {"$group": {"_id": "$query_text", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": limit}
            ]
            return list(self.mongo_collection.aggregate(pipeline))
        except Exception as e:
            print("Ошибка получения топ жанр+год:", e)
            return []

    def close_connection(self):
        """Закрытие соединений с базами данных."""
        if self.mysql_conn:
            self.mysql_conn.close()
            print("Подключение MySQL закрыто.")
        if self.mongo_client:
            self.mongo_client.close()
            print("Подключение Mongo закрыто.")
            print("До скорой встрече!")