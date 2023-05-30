import random
import string

from flask import redirect, render_template, url_for

from yacut import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        url_map = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        return redirect(url_for('redirect_to_url', short_id=custom_id))
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map:
        return redirect(url_map.original)
    else:
        # Обработка случая, когда короткий идентификатор не существует
        return render_template('not_found.html')
