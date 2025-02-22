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
pip install -r requirements.txt
```

Файл `requirements.txt` включает:
- `wxPython` — для графического интерфейса.
- `pymysql` — для работы с MySQL.
- `pymongo` и `dnspython` — для взаимодействия с MongoDB.

## Настройка
### 1. Конфигурация базы данных
Перед запуском создайте файл `.env` в корневой директории проекта и укажите параметры подключения:

```env
HOST=your-mysql-host
USER=your-mysql-user
PASSWORD=your-mysql-password
DATABASE=sakila

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB=search_queries_db
MONGO_COLLECTION=queries
```

### 2. Запуск приложения
Запустите `main.py`:

```bash
python main.py
```

## Структура проекта
```
.
├── main.py            # Главный файл запуска GUI
├── display.py         # Интерфейс приложения (wxPython)
├── command_handler.py # Обработчик команд
├── db_handler.py      # Работа с MySQL и MongoDB
├── connection.py      # Установление соединений с БД
├── config.py          # Конфигурация окружения
├── requirements.txt   # Зависимости проекта
├── .gitignore         # Игнорируемые файлы
└── .env               # Конфигурация базы данных (не хранить в репозитории)
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

