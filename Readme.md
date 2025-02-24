# Film Search (Sakila)

Этот проект представляет собой графическое приложение для поиска фильмов в базе данных Sakila. Он использует `wxPython` для интерфейса, MySQL для хранения данных о фильмах и MongoDB для сохранения поисковых запросов.

## Функциональность
- Поиск фильмов по названию.
- Фильтрация фильмов по жанру и году выпуска.
- Отображение популярных запросов.
- Подключение к MySQL и MongoDB.

## Требования
Для работы проекта требуется установка следующих зависимостей:
```bash
python -m venv venv
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Файл `requirements.txt` включает:
- `wxPython` — для графического интерфейса.
- `pymysql` — для работы с MySQL.
- `pymongo`  — для взаимодействия с MongoDB.
- `python-dotenv` — загружает переменные окружения из .env.

## Настройка
### 1. Конфигурация базы данных
Перед запуском создайте файл `.env` в корневой директории проекта и укажите параметры подключения:

Создайте свою локальную Базу Данных в MongoDB и измените названия базы данных
```env
HOST=your-mysql-host
USER=your-mysql-user
PASSWORD=your-mysql-password
DATABASE=sakila

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=search_queries_db  # Измените на свои данные
MONGO_COLLECTION=queries    # Измените на свои данные
```

### 2. Запуск приложения
Запустите `main.py`:

```bash
python main.py
```

## Структура проекта
```
.
├── data_base/
│   ├── __init__.py
│   ├── config.py          # Конфигурация окружения
│   ├── connection.py      # Установление соединений с БД
│   └── db_handler.py      # Работа с MySQL и MongoDB
├── GUI/
│   ├── __init__.py
│   └── display.py         # Интерфейс приложения (wxPython)
├── services/
│   ├── __init__.py
│   └── command_handler.py # Обработчик команд
├── .gitignore             # Игнорируемые файлы
├── .env                   # Конфигурация базы данных (не хранить в репозитории)
├── main.py                # Главный файл запуска GUI
├── Readme.md              # Документация
└── requirements.txt       # Зависимости проекта
```

## Основные файлы
### `main.py`
Запускает GUI-приложение, созданное с использованием `wxPython`.

### `display.py`
- Создает пользовательский интерфейс.
- Подключается к `CommandHandler` для обработки запросов.
- Позволяет пользователю искать фильмы по названию, жанру и году.

### `command_handler.py`
- Связывает интерфейс с базой данных.
- Выполняет поиск фильмов по разным параметрам.
- Обрабатывает популярные запросы.

### `db_handler.py`
- Выполняет SQL-запросы к MySQL (поиск по названию, жанру, году и т. д.).
- Сохраняет поисковые запросы в MongoDB.

### `connection.py`
- Устанавливает соединение с MySQL и MongoDB.
- Загружает параметры из `config.py`.

### `config.py`
- Загружает параметры окружения из `.env`.
- Определяет конфигурацию MySQL и MongoDB.

## Дополнительная информация
- Если `wxPython` не устанавливается через `pip`, установите его вручную с [официального сайта](https://wxpython.org/pages/downloads/).
- База данных Sakila должна быть предварительно загружена в MySQL.
- MongoDB используется для хранения истории запросов и популярных поисков.

## Автор
### Vatov Petru

Проект разработан в образовательных целях.

