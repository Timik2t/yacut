from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired, Optional, Regexp, Length

from .constants import CUSTOM_ID_PATTERN


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Исходная ссылка',
        validators=[DataRequired(message='Обязательное поле'), URL()]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[
            Optional(),
            Regexp(
                CUSTOM_ID_PATTERN,
                message='Поле должно содержать 6 символов: большие и маленькие латинские буквы, цифры'
            ),
            Length(max=16, message='Максимальная длина пользовательской ссылки - 16 символов')
        ]
    )
    submit = SubmitField('Создать')
