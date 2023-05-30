import random
import string

from flask import redirect, render_template, url_for

from yacut import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import SHORT_ID_LENGTH


def get_unique_short_id(length=SHORT_ID_LENGTH):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(chars, k=length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        db.session.add(URLMap(original=form.original_link.data, short=custom_id))
        db.session.commit()
        return redirect(url_for('redirect_to_url', short_id=custom_id))
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_to_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    if not url_map:
        return render_template('not_found.html')
    return redirect(url_map.original)
