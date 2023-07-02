import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import check_unique_short_id, get_unique_short_id

LINK_PATTERN = r'^[a-zA-Z\d]{1,16}$'


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """
    Функция для реализации GET-запроса на получение
    оригинальной длинной ссылки по указанному короткому идентификатору.
    """

    url_map_obj = URLMap.query.filter_by(short=short_id).first()
    if url_map_obj is None:
        raise InvalidAPIUsage('В базе данных нет такой ссылки', 404)
    original_link = url_map_obj.original
    return jsonify({'url': original_link}), 200


@app.route('/api/id/', methods=['POST'])
def add_url():
    """
    Функция для реализации POST-запроса на создание новой короткой ссылки.
    """

    data = request.get_json()
    if not data:
        raise InvalidAPIUsage("Отсутствую данные в теле запроса.")
    if 'url' not in data:
        raise InvalidAPIUsage("Отсутствует обязательная оригинальная ссылка в теле запроса.")
    if 'custom_id' in data:
        custom_id = data.get('custom_id')
        if not check_unique_short_id(custom_id):
            raise InvalidAPIUsage(f'Имя короткой ссылки "{custom_id}" уже занято.')
        if custom_id == "" or custom_id is None:
            data['custom_id'] = get_unique_short_id()
        elif not re.match(LINK_PATTERN, custom_id):
            raise InvalidAPIUsage('Недопустимое имя для короткой ссылки')
    else:
        data['custom_id'] = get_unique_short_id()

    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), 201
