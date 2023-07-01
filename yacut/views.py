import random
import string

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap

ALLOWEED_SYMBOLS = string.ascii_letters + string.digits
LEN_OF_SHORT_ID = 6


@app.route('/', methods=['GET', 'POST'])
def main_view():
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
    return render_template('main_page.html', form=form)


@app.route('/<short_id>')
def follow_link(short_id):
    """Функция, которая отвечает за переадресацию."""
    object_in_db = URLMap.query.filter_by(short=short_id).first_or_404()
    original_link = object_in_db.original
    return redirect(original_link)


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
    short = "".join(random.choices(string.ascii_lowercase, k=6))
    if URLMap.query.filter_by(short=short).first():
        get_unique_short_id()
    return short




# import random
# import string

# from flask import flash, redirect, render_template

# from . import app, db
# from .forms import URLMapForm
# from .models import URLMap

# # добавляем 2 константы
# # ALLOWEED_SYMBOLS представляет из себя строку из прописных и заглавных
# # латинских букв и из цифр от 0 до 9. Эта константа будет использована
# # для генерации уникального короткого идентификатора с помощью
# # random.choice()
# ALLOWEED_SYMBOLS = string.ascii_letters + string.digits
# LEN_OF_SHORT_ID = 6


# # напишем функцию проверки уникальности короткого идентификатора
# # так как использование этой логики понадобится в нескольктх местах,
# def check_unique_short_id(short_id):
#     """
#     Функция для проверки уникальности короткого идентификатора.
#     """
#     # если среди объектов модели URLMap в базе данных уже есть
#     # объект с таким же коротким идентификатором, то вернуть True
#     # в противном случае вернуть False
#     # далее эту функцию можно использовать для проверки уникальности
#     # короткого идентификатора
#     if URLMap.query.filter_by(short=short_id).first() is None:
#         return True
#     return False


# # напишем функцию для генерации короткого идентификатора ссылки
# # используем метод random.choice и заготовленные константы
# # для генерации короткого идентификатора
# # далее проверка на уникального сгенерированного идентификатора
# # если он уникален, то вернем этот идентификатор
# # если нет - генерируем заново с помощью функции get_unique_short_id
# def get_unique_short_id():
#     """
#     Функция генерации уникального короткого идентификатора из 6 символов.
#     """
#     short = "".join(random.choices(
#         ALLOWEED_SYMBOLS, LEN_OF_SHORT_ID))
#     if URLMap.query.filter_by(short=short).first():
#         get_unique_short_id()
#     return short
#     # short_id = ''.join(random.choice(
#     #     ALLOWEED_SYMBOLS) for i in range(LEN_OF_SHORT_ID))
#     # if check_unique_short_id(short_id):
#     #     return short_id
#     # return get_unique_short_id()


# # функция, которая отвечает за отображение главной страницы с формой
# # используем декоратор @app.route, который связывает функцию,которая
# # обернута в декоратор с указанным URL
# # указываем методы запросов
# @app.route('/', methods=['GET', 'POST'])
# def main_view():

#     #"""Функция, которая отвечает за отображение главной страницы."""
#     @app.route('/', methods=['GET', 'POST'])
#     def main_view():
#         form = URLMapForm()
#         if form.validate_on_submit():
#             short = form.custom_id.data
#             if not short:
#                 short = get_unique_short_id()
#             urlmap = URLMap(original=form.original_link.data, short=short)
#             db.session.add(urlmap)
#             db.session.commit()
#         return render_template("main_page.html", form=form)
#     # form = URLMapForm()
#     # # проверка на валидность:
#     # # если при заполнении формы возникли ошибки,
#     # # то есть, если метод validate_on_submit вернет False
#     # # (не все обязательные поля формы заполнены или заполнены некорректно),
#     # # то нужно вернуть пользователя на главную страницу с пустой формой
#     # # для повторного заполнения

#     # if not form.validate_on_submit():
#     #     return render_template('main_page.html', form=form)
#     # # # в переменной short сохраним значение короткого идентификатора ссылки из данных,
#     # # #  которые пользователь ввел в форму -
#     # # # так как именно эти данные должны быть проверены далее на уникальность
#     # custom_id = form.custom_id.data
#     # # # если в data нет short, то есть, если пользователь не ввел короткий идентификатор
#     # # # то нужно сгенерировать уникальный рандомный идентификатор custom_id
#     # # #  с помощью функции get_unique_short_id
#     # if not custom_id:
#     #     custom_id = get_unique_short_id()
#     # elif not check_unique_short_id(custom_id):
#     #     # выполним проверку на уникальность -
#     #     # если в базе данных уже есть объект URLMap с указанным коротким индентификатором,
#     #     # то вернется флэш-сообщение о том, что поле short не уникально
#     #     flash(f'Имя идентификатора {custom_id} уже занято!', 'link-taken')
#     #     # и вернем пользователя на главную страницу с формой,
#     #     # чтобы пользователь ввел другой короткий идентификатор
#     #     return render_template('main_page.html', form=form)
#     # # если же в базе нет объекта с таким коротким идентификатором,
#     # # то есть, введенный идентификатор уникален,
#     # # то создаем этот экземпляр модели в БД,
#     # url_map = URLMap(
#     #     original=form.original_link.data,
#     #     short=custom_id
#     # )
#     # # сохраняем и комитим посредством сессии
#     # db.session.add(url_map)
#     # db.session.commit()
#     # return render_template('main_page.html', form=form)


# @app.route('/<short_id>')
# def follow_link(short_id):
#     """Функция, которая отвечает за переадресацию."""
#     object_in_db = URLMap.query.filter_by(short=short_id).first_or_404()
#     original_link = object_in_db.original
#     return redirect(original_link)
