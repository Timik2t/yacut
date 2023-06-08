# YaCut

## Описание

Сервис укорачивания ссылок с web интерфейсом и REST API. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

Возможности:

- Генерация коротких ссылок и связь их с исходными длинными ссылками
- Переадресация на исходный адрес при обращении к коротким ссылкам
- Доступны web и api интерфейсы.

## Технологии

Python

FLASK

Jinja2

SQLAlchemy

REST


## Подготовка и запуск проекта

### Склонировать репозиторий на локальную машину

```
git clone git@github.com:Timik2t/yacut.git
```

В корневой папке проекта нужно создать виртуальное окружение и установить зависимости.

```
python -m venv venv
```

и

```
pip install -r requirements.txt
```

В корне проекта создайте `.env` файл**
```
FLASK_APP=yacut
FLASK_DEBUG=1
DATABASE_URI=<URI базы данных, по умолчанию "sqlite:///db.sqlite3">
SECRET_KEY=<секретный ключ>
```

### Запуск

Выполнить миграции:
````
flask db upgrade
```

Запуск сервиса:
```
flask run
```

### Справка

![Usage-example](docs/usage_example.gif)

### API (Docs: [OpenAPI](docs/openapi.yml))

- **POST** `/api/id/`
- **GET** `/api/id/{short_id}/`

### Автор
[Исхаков Тимур](https://github.com/Timik2t "GitHub аккаунт")