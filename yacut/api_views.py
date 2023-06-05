from http import HTTPStatus
from re import match

from flask import jsonify, request

from . import app
from .constants import SHORT_URL_API_PATTERN
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import add_to_db, get_unique_short_id

INVALID_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_ORIGINAL_URL = '"url" является обязательным полем!'
SHORT_URL_ALREADY_EXISTS = 'Такой URL уже занят'
URL_NOT_FOUND = 'Указанный id не найден'
INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_NAME = 'Имя "{}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)

    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(MISSING_ORIGINAL_URL)

    if 'custom_id' not in data or not data['custom_id']:
        short_id = get_unique_short_id()
        data['custom_id'] = short_id

    if not match(SHORT_URL_API_PATTERN, data['custom_id']):
        raise InvalidAPIUsage(INVALID_CUSTOM_ID)

    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(UNIQUE_NAME.format(data['custom_id']))

    new_url = URLMap()
    new_url.from_dict(data)
    add_to_db(new_url)
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(URL_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
