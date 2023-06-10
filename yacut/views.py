from flask import flash, redirect, render_template, url_for

from yacut import app

from .constants import REDIRECT_URL_MAP
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short=url_for(
                REDIRECT_URL_MAP,
                short=URLMap.create(
                    original=form.original_link.data,
                    short=form.custom_id.data,
                    is_valid=True
                ).short,
                _external=True,
            )
        )
    except ValueError as error:
        flash(error)


@app.route('/<string:short>', methods=['GET'])
def redirect_to_url(short):
    return redirect(URLMap.find_or_404(short).original)
