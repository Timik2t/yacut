from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    URL, DataRequired, Length,
    Optional, Regexp, ValidationError
)

from .constants import MAX_SHORT_LENGTH, ORIGINAL_LENGTH, SHORT_PATTERN
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
                SHORT_PATTERN,
                message=CUSTOM_ID_REQUIRED
            ),
            Length(
                max=MAX_SHORT_LENGTH,
                message=CUSTOM_LENGTH.format(MAX_SHORT_LENGTH)
            )
        ]
    )
    submit = SubmitField('Создать')

    def validate_custom_id(self, field):
        if field.data and URLMap.get_short_url_map(field.data):
            raise ValidationError(UNIQUE_NAME.format(field.data))
