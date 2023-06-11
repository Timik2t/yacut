import random
from datetime import datetime
from re import match

from flask import url_for

from yacut import db

from .constants import (
    DEFAULT_SHORT_LENGTH, MAX_ATTEMPTS, MAX_SHORT_LENGTH,
    ORIGINAL_LENGTH, REDIRECT_URL_MAP, SHORT_PATTERN,
    VALID_CHARS
)

INVALID_SHORT_СHARS = 'Указано недопустимое имя для короткой ссылки'
UNIQUE_NAME = 'Имя "{}" уже занято.'
WRONG_ORIGINAL_LENGTH = 'Превышена длина оригинальной ссылки '
GET_SHORT_FAULT = 'Не удалось создать короткую ссылку'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LENGTH), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                REDIRECT_URL_MAP,
                short=self.short,
                _external=True
            )
        )

    @staticmethod
    def create(original, short=None, is_valid=False):
        if len(original) > ORIGINAL_LENGTH:
            raise ValueError(WRONG_ORIGINAL_LENGTH)
        if not short:
            short = URLMap.get_unique_short()
        elif not is_valid:
            if len(short) > MAX_SHORT_LENGTH:
                raise ValueError(
                    INVALID_SHORT_СHARS.format(
                        user_short_length=len(short)
                    )
                )
            if not match(SHORT_PATTERN, short):
                raise ValueError(INVALID_SHORT_СHARS)
            if URLMap.get(short):
                raise ValueError(UNIQUE_NAME.format(short))
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def find_or_404(short_id):
        return URLMap.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def get_unique_short(
        chars=VALID_CHARS,
        length=DEFAULT_SHORT_LENGTH,
        max_attempts=MAX_ATTEMPTS
    ):
        for _ in range(max_attempts):
            short_id = ''.join(random.choices(chars, k=length))
            if not URLMap.get(short_id):
                return short_id
        raise ValueError(GET_SHORT_FAULT)
