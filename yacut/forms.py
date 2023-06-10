from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import (
    URL, DataRequired, Length,
    Optional, Regexp, ValidationError
)

from .constants import (
    DEFAULT_SHORT_LENGTH, MAX_SHORT_LENGTH,
    ORIGINAL_LENGTH, SHORT_PATTERN
)
from .models import URLMap

DESCRIPTION_ORIGINAL_LINK = 'Исходная ссылка'
DESCRIPTION_CUSTOM_ID = 'Ваш вариант короткой ссылки'
ORIGINAL_LINK_REQUIRED = 'Обязательное поле'
INVALID_LENGTH = 'Максимальная длина пользовательской ссылки - {} символов'
INVALID_ORIGINAL_LENGTH = INVALID_LENGTH.format(ORIGINAL_LENGTH)
INVALID_SHORT_LENGTH = INVALID_LENGTH.format(MAX_SHORT_LENGTH)
CUSTOM_ID_REQUIRED = (
    f'Поле должно содержать {DEFAULT_SHORT_LENGTH} символов: '
    'большие и маленькие латинские буквы, цифры'
)
URL_ONLY = 'Поле должно содержать URL адрес'
UNIQUE_NAME = 'Имя {} уже занято!'
SUMBIT = 'Создать'


class URLMapForm(FlaskForm):
    original_link = URLField(
        DESCRIPTION_ORIGINAL_LINK,
        validators=[
            DataRequired(message=ORIGINAL_LINK_REQUIRED),
            URL(require_tld=True, message=URL_ONLY),
            Length(
                max=ORIGINAL_LENGTH,
                message=INVALID_ORIGINAL_LENGTH
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
                message=INVALID_SHORT_LENGTH
            )
        ]
    )
    submit = SubmitField(SUMBIT)

    def validate_custom_id(self, field):
        if field.data and URLMap.get(field.data):
            raise ValidationError(UNIQUE_NAME.format(field.data))
