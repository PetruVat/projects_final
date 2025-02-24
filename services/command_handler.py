from data_base.db_handler import DBHandler


class CommandHandler:
    def __init__(self):
        self.db = DBHandler()

    def search_keyword_no_save(self, keyword):
        results = self.db.search_by_keyword(keyword)
        return results

    def save_query_only(self, query_text, query_type):
        self.db.save_search_query(query_text, query_type)

    def search_genre_year(self, genre, year):
        results = self.db.search_by_genre_year(genre, year)
        self.db.save_search_query(f"{genre}, {year}", "search_genre_year")
        return results

    def search_year(self, year):
        results = self.db.search_year(year)
        self.db.save_search_query(year, "search_year")
        return results

    def search_genre(self, genre):
        results = self.db.search_genre(genre)
        self.db.save_search_query(genre, "search_genre")
        return results

    def get_popular_queries(self):
        return self.db.get_popular_queries()

    def get_years(self):
        return self.db.get_years()

    def get_genres(self):
        return self.db.get_genres()

    def get_top_keywords(self):
        return self.db.get_top_keywords_mongo()

    def get_top_genres_year(self):
        return self.db.get_top_genres_years_mongo()

    def close(self):
        self.db.close_connection()

