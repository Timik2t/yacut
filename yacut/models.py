import random
from datetime import datetime
from re import match

from flask import url_for

from yacut import db

from .constants import (
    CHARS, CUSTOM_ID_PATTERN,
    DEFAULT_SHORT_LINK_LENGTH,
    MAX_ATTEMPTS, ORIGINAL_LENGTH,
    REDIRECT_URL, USERS__SHORT_LINK_LENGTH
)
from .error_handlers import InvalidAPIUsage

INVALID_CUSTOM_ID = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_NAME = 'Имя "{}" уже занято.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(USERS__SHORT_LINK_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_URL,
                short_id=self.short,
                _external=True
            )
        )

    @staticmethod
    def from_dict(data):
        original_url = data['url']
        custom_id = data.get('custom_id')
        if custom_id:
            if URLMap.is_short_id_taken(custom_id):
                raise InvalidAPIUsage(UNIQUE_NAME.format(custom_id))
            if not match(CUSTOM_ID_PATTERN, custom_id) or len(custom_id) > USERS__SHORT_LINK_LENGTH:
                raise InvalidAPIUsage(INVALID_CUSTOM_ID)
        else:
            custom_id = URLMap.get_unique_short_id()
            data['custom_id'] = custom_id
        return URLMap(original=original_url, short=custom_id)

    @staticmethod
    def is_short_id_taken(short_id):
        return URLMap.query.filter_by(short=short_id).first() is not None

    @staticmethod
    def find_by_short_id(short_id):
        return URLMap.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def get_unique_short_id(
        chars=CHARS,
        length=DEFAULT_SHORT_LINK_LENGTH,
        max_attempts=MAX_ATTEMPTS
    ):
        for _ in range(max_attempts):
            short_id = ''.join(random.choices(chars, k=length))
            if not URLMap.is_short_id_taken(short_id):
                return short_id

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def create_from_form(form):
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if custom_id and URLMap.is_short_id_taken(custom_id):
            return None
        elif not custom_id:
            custom_id = URLMap.get_unique_short_id()
        return URLMap(original=original_link, short=custom_id)
