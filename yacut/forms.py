from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp, ValidationError

from .constants import (
    CUSTOM_ID_PATTERN, ORIGINAL_LENGTH,
    USERS__SHORT_LINK_LENGTH
)
from .models import URLMap

DESCRIPTION_ORIGINAL_LINK = 'Исходная ссылка'
DESCRIPTION_CUSTOM_ID = 'Ваш вариант короткой ссылки'
ORIGINAL_LINK_REQUIRED = 'Обязательное поле'
CUSTOM_LENGTH = 'Максимальная длина пользовательской ссылки - {} символов'
CUSTOM_ID_REQUIRED = 'Поле должно содержать 6 символов: большие и маленькие латинские буквы, цифры'
URL_ONLY = 'Поле должно содержать URL адрес'
UNIQUE_NAME = 'Имя {} уже занято!'


class URLMapForm(FlaskForm):
    original_link = URLField(
        DESCRIPTION_ORIGINAL_LINK,
        validators=[
            DataRequired(message=ORIGINAL_LINK_REQUIRED),
            URL(require_tld=True, message=URL_ONLY),
            Length(
                max=ORIGINAL_LENGTH,
                message=CUSTOM_LENGTH.format(ORIGINAL_LENGTH)
            )
        ]
    )
    custom_id = URLField(
        DESCRIPTION_CUSTOM_ID,
        validators=[
            Optional(),
            Regexp(
                CUSTOM_ID_PATTERN,
                message=CUSTOM_ID_REQUIRED
            ),
            Length(
                max=USERS__SHORT_LINK_LENGTH,
                message=CUSTOM_LENGTH.format(USERS__SHORT_LINK_LENGTH)
            )
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.is_short_id_taken(field.data):
            raise ValidationError(UNIQUE_NAME.format(field.data))
