from flask import flash, redirect, render_template

from yacut import app

from .forms import URLMapForm
from .models import URLMap

UNIQUE_NAME = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            original=form.original_link.data,
            short=form.custom_id.data,
            valid_form=True
        )
    except ValueError as error:
        flash(error)
    return render_template('index.html', form=form, short=url_map.short)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(URLMap.find_by_short_id_or_404(short).original)
