from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

INVALID_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_ORIGINAL_URL = '"url" является обязательным полем!'
SHORT_URL_ALREADY_EXISTS = 'Такой URL уже занят'
URL_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(MISSING_ORIGINAL_URL)
    new_url = URLMap.from_dict(data)
    new_url.add_to_db()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage(URL_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
