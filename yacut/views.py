import random
import string

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap

ALLOWEED_SYMBOLS = string.ascii_letters + string.digits
LEN_OF_SHORT_ID = 6


def check_unique_short_id(short_id):
    """
    Функция для проверки уникальности короткого идентификатора.
    """

    if URLMap.query.filter_by(short=short_id).first() is None:
        return True
    return False


def get_unique_short_id():
    """
    Функция генерации уникального короткого идентификатора из 6 символов.
    """

    short_id = ''.join(random.choice(
        ALLOWEED_SYMBOLS) for i in range(LEN_OF_SHORT_ID))
    if check_unique_short_id(short_id):
        return short_id
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def main_view():
    """
    Функция, которая отвечает за отображение главной страницы.
    """

    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('main_page.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    elif not check_unique_short_id(custom_id):
        flash(f'Имя идентификатора {custom_id} уже занято!', 'link-taken')
        return render_template('main_page.html', form=form)
    url_map = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url_map)
    db.session.commit()
    return render_template('main_page.html', url=url_map, form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    """
    Функция, которая отвечает за переадресацию.
    """

    object_in_db = URLMap.query.filter_by(short=short_id).first_or_404()
    original_link = object_in_db.original
    return redirect(original_link)
