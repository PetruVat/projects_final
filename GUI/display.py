import wx
from services.command_handler import CommandHandler

class Application(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Film Search (Sakila)", size=(900, 650))
        self.cmd_handler = CommandHandler()


        self.SetBackgroundColour("#FFFFFF")
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#FFFFFF")
        main_sizer = wx.BoxSizer(wx.VERTICAL)


        top_panel = wx.Panel(panel)
        top_panel.SetBackgroundColour("#F3F3F3")
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)


        font_header = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="Segoe UI")
        font_label = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Segoe UI")


        name_sizer = wx.BoxSizer(wx.VERTICAL)
        name_label = wx.StaticText(top_panel, label="🔎 Поиск по названию")
        name_label.SetFont(font_label)
        self.name_input = wx.TextCtrl(top_panel, size=(250, -1))
        self.name_input.SetBackgroundColour("#FFFFFF")
        self.name_input.SetForegroundColour("#333333")
        name_sizer.Add(name_label, 0, wx.ALL, 5)
        name_sizer.Add(self.name_input, 0, wx.ALL | wx.EXPAND, 5)


        year_sizer = wx.BoxSizer(wx.VERTICAL)
        year_label = wx.StaticText(top_panel, label="📅 Выберите Год")
        year_label.SetFont(font_label)
        years = [""] + self.cmd_handler.get_years()
        self.year_choice = wx.Choice(top_panel, choices=years)
        self.year_choice.SetBackgroundColour("#FFFFFF")
        year_sizer.Add(year_label, 0, wx.ALL, 5)
        year_sizer.Add(self.year_choice, 0, wx.ALL | wx.EXPAND, 5)


        genre_sizer = wx.BoxSizer(wx.VERTICAL)
        genre_label = wx.StaticText(top_panel, label="🎭 Жанр")
        genre_label.SetFont(font_label)
        genres = [""] + self.cmd_handler.get_genres()
        self.genre_choice = wx.Choice(top_panel, choices=genres)
        self.genre_choice.SetBackgroundColour("#FFFFFF")
        genre_sizer.Add(genre_label, 0, wx.ALL, 5)
        genre_sizer.Add(self.genre_choice, 0, wx.ALL | wx.EXPAND, 5)


        self.top_button = wx.Button(top_panel, label="🔥 Топ запросы", size=(120, 35))
        self.top_button.SetBackgroundColour("#0078D7")
        self.top_button.SetForegroundColour("#FFFFFF")
        self.top_button.SetFont(font_label)
        self.top_button.SetWindowStyleFlag(wx.BORDER_NONE)


        top_sizer.Add(name_sizer, 1, wx.ALL | wx.EXPAND, 10)
        top_sizer.Add(year_sizer, 1, wx.ALL | wx.EXPAND, 10)
        top_sizer.Add(genre_sizer, 1, wx.ALL | wx.EXPAND, 10)
        top_sizer.Add(self.top_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 20)
        top_panel.SetSizer(top_sizer)


        result_panel = wx.Panel(panel)
        result_panel.SetBackgroundColour("#FFFFFF")
        result_sizer = wx.BoxSizer(wx.VERTICAL)
        result_label = wx.StaticText(result_panel, label="📋 Результат поиска:")
        result_label.SetFont(font_header)
        self.result_box = wx.TextCtrl(result_panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 250))
        self.result_box.SetBackgroundColour("#FFFFFF")
        self.result_box.SetForegroundColour("#333333")
        result_sizer.Add(result_label, 0, wx.ALL, 5)
        result_sizer.Add(self.result_box, 1, wx.ALL | wx.EXPAND, 5)
        result_panel.SetSizer(result_sizer)


        main_sizer.Add(top_panel, 0, wx.EXPAND | wx.ALL, 15)
        main_sizer.Add(result_panel, 1, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(main_sizer)


        self.name_input.Bind(wx.EVT_TEXT, self.on_update_search)
        self.year_choice.Bind(wx.EVT_CHOICE, self.on_update_search)
        self.genre_choice.Bind(wx.EVT_CHOICE, self.on_update_search)
        self.top_button.Bind(wx.EVT_BUTTON, self.on_top_queries)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Show()

    def on_update_search(self, event):
        """
        Обновление результатов поиска при каждом изменении ввода:
         - Если введено ключевое слово – поиск по ключевому слову.
         - Если выбраны год и жанр – поиск по жанру и году.
         - Если выбран только год – поиск по году.
         - Если выбран только жанр – поиск по жанру.
        """
        keyword = self.name_input.GetValue().strip()
        year_index = self.year_choice.GetSelection()
        genre_index = self.genre_choice.GetSelection()
        year_val = self.year_choice.GetStringSelection() if year_index != wx.NOT_FOUND else ""
        genre_val = self.genre_choice.GetStringSelection() if genre_index != wx.NOT_FOUND else ""

        if keyword:
            results = self.cmd_handler.search_keyword(keyword)
            self.display_films(results)
        elif year_val and genre_val:
            results = self.cmd_handler.search_genre_year(genre_val, year_val)
            self.display_films(results)
        elif year_val:
            results = self.cmd_handler.search_year(year_val)
            self.display_films(results)
        elif genre_val:
            results = self.cmd_handler.search_genre(genre_val)
            self.display_films(results)
        else:
            self.result_box.SetValue("")

    def on_top_queries(self, event):
        """Отображение популярных запросов."""
        popular_queries = self.cmd_handler.get_popular_queries()
        display_text = "Популярные запросы:\n\n"
        for query in popular_queries:
            display_text += f"{query['_id']} — {query['count']} раз\n"
        self.result_box.SetValue(display_text)

    def display_films(self, films):
        self.result_box.Clear()
        if films:
            output = "Найденные фильмы:\n\n"
            for film in films:
                title = film.get("title", "Без названия")
                description = film.get("description", "Нет описания")
                release_year = film.get("release_year", "Не указан")
                genre = film.get("genre", "")
                output += f"Название: {title}\n"
                output += f"Описание: {description}\n"
                output += f"Год выпуска: {release_year}\n"
                if genre:
                    output += f"Жанр: {genre}\n"
                output += "-" * 40 + "\n"
            self.result_box.SetValue(output)
        else:
            self.result_box.SetValue("Фильмы не найдены.")

    def on_close(self, event):
        self.cmd_handler.close()
        self.Destroy()


