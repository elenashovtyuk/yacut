from flask import render_template
from . import app
from .forms import URLMapForm

# функция, которая отвечает за отображение главной страницы с формой
# используем декоратор @app.route, который связывает функцию,которая
# обернута в декоратор с указанным URL
@app.route('/')
def main_view():
    form = URLMapForm()
    return render_template('index.html', form=form)
