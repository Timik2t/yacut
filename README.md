# YaCut

## Описание проекта

Сервис укорачивания ссылок с web интерфейсом и REST API. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

### Возможности

- Генерация коротких ссылок и связь их с исходными длинными ссылками
- Переадресация на исходный адрес при обращении к коротким ссылкам
- Доступны web и api интерфейсы

## Технологии

- Python
- FLASK
- Jinja2
- SQLAlchemy

## Подготовка и запуск проекта

1. Склонируйте репозиторий на локальную машину:

    ```bash
    git clone git@github.com:Timik2t/yacut.git
    ```

2. Создайте и активируйте виртуальное окружение:

    ```bash
    python -m venv venv
    ```

    Активация окружения
    ```bash
    # Windows
    source venv/Scripts/activate
    ```
    ```bash
    # Linux
    source venv/bin/activate
    ```
3. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```
4. Примените миграции:

    ```bash
    flask db upgrade
    ```
5. Создайте файл с переменными окружения `.env` и заполните его данными:

    ```bash
    FLASK_APP=yacut
    FLASK_DEBUG=1
    DATABASE_URI=<URI базы данных, по умолчанию "sqlite:///db.sqlite3">
    SECRET_KEY=<секретный ключ>
    ```
6. Запуск проекта:

    Стандартный запуск:
    ```bash
    flask run
    ```

### API (Docs: [OpenAPI](openapi.yml))

- **POST** `/api/id/`
- **GET** `/api/id/{short_id}/`

### Автор

[Исхаков Тимур](https://github.com/Timik2t "GitHub аккаунт")
