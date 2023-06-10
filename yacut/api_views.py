from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

INVALID_SHORT_URL = 'Указано недопустимое имя для короткой ссылки'
MISSING_REQUEST_BODY = 'Отсутствует тело запроса'
MISSING_ORIGINAL_URL = '"url" является обязательным полем!'
URL_NOT_FOUND = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage(MISSING_REQUEST_BODY)
    if 'url' not in data or not data['url']:
        raise InvalidAPIUsage(MISSING_ORIGINAL_URL)
    try:
        return jsonify(
            URLMap.create(
                data['url'],
                data.get('custom_id')
            ).to_dict()
        ), HTTPStatus.CREATED
    except ValueError as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.get(short_id)
    if not url_map:
        raise InvalidAPIUsage(URL_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
