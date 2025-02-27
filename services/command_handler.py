from data_base.db_handler import DBHandler


class CommandHandler:
    """Класс обработки команд, взаимодействующий с базой данных."""
    def __init__(self):
        """Инициализация обработчика команд и создание подключения к БД."""
        self.db = DBHandler()

    def search_keyword_no_save(self, keyword):
        """Поиск фильмов по ключевому слову без сохранения запроса."""
        results = self.db.search_by_keyword(keyword)
        return results

    def save_query_only(self, query_text, query_type):
        """Сохранение поискового запроса в базе данных без выполнения поиска."""
        self.db.save_search_query(query_text, query_type)

    def search_genre_year(self, genre, year):
        """Поиск фильмов по жанру и году с сохранением запроса в БД."""
        results = self.db.search_by_genre_year(genre, year)
        self.db.save_search_query(f"{genre}, {year}", "search_genre_year")
        return results

    def search_year(self, year):
        """Поиск фильмов по году с сохранением запроса в БД."""
        results = self.db.search_year(year)
        self.db.save_search_query(year, "search_year")
        return results

    def search_genre(self, genre):
        """Поиск фильмов по жанру с сохранением запроса в БД."""
        results = self.db.search_genre(genre)
        self.db.save_search_query(genre, "search_genre")
        return results

    def get_popular_queries(self):
        """Получение популярных запросов из базы данных."""
        return self.db.get_popular_queries()

    def get_years(self):
        """Получение списка доступных лет выпуска фильмов."""
        return self.db.get_years()

    def get_genres(self):
        """Получение списка доступных жанров фильмов."""
        return self.db.get_genres()

    def get_top_keywords(self):
        """Получение топ-ключевых слов для поиска из MongoDB."""
        return self.db.get_top_keywords_mongo()

    def get_top_genres_year(self):
        """Получение топовых запросов по жанру и году из MongoDB."""
        return self.db.get_top_genres_years_mongo()

    def close(self):
        """Закрытие соединения с базой данных."""
        self.db.close_connection()

