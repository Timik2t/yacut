import random
import string

from sqlalchemy.exc import IntegrityError

from . import db
from .constants import SHORT_ID_LENGTH
from .error_handlers import DatabaseError
from .models import URLMap

ADD_TO_DB_ERROR = 'Ошибка добавдения в базу данных {error}'


def get_unique_short_id(length=SHORT_ID_LENGTH):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


def add_to_db(url):
    try:
        db.session.add(url)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise DatabaseError(ADD_TO_DB_ERROR.format(error)) from error
