from flask import abort, flash, redirect, render_template, url_for

from yacut import app

from .forms import URLMapForm
from .models import URLMap
from .constants import REDIRECT_URL

UNIQUE_NAME = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        new_url = URLMap.create_from_form(form)
        if new_url:
            new_url.add_to_db()
            return render_template(
                'index.html',
                form=form,
                short_link=url_for(REDIRECT_URL, short_id=new_url.short, _external=True)
            )
        else:
            flash(UNIQUE_NAME.format(form.custom_id.data), 'danger')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def redirect_to_url(short_id):
    redirect_url = URLMap.find_by_short_id(short_id)
    if not redirect_url:
        abort(404)
    return redirect(redirect_url.original)
