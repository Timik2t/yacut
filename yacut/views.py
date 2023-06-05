from flask import abort, flash, redirect, render_template, url_for

from yacut import app

from .forms import URLMapForm
from .models import URLMap
from .utils import add_to_db, get_unique_short_id

UNIQUE_NAME = 'Имя {} уже занято!'


def render_index_template(form):
    return render_template('index.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_index_template(form)
    return handle_valid_form_submission(form)


def handle_valid_form_submission(form):
    short_id = form.custom_id.data or get_unique_short_id()
    if URLMap.query.filter_by(short=short_id).first():
        flash(UNIQUE_NAME.format(short_id), 'danger')
        return render_index_template(form)
    new_url = URLMap(
        original=form.original_link.data,
        short=short_id,
    )
    add_to_db(new_url)
    flash(url_for('redirect_to_url', short_id=short_id, _external=True), 'result')
    return render_index_template(form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_to_url(short_id):
    redirect_url = URLMap.query.filter_by(short=short_id).first_or_404()
    if not redirect_url:
        abort(404)
    return redirect(redirect_url.original)
