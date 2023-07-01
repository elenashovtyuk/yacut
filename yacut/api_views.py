# импортируем метод, который позволяет преобразовать словарь Python в JSON
from flask import jsonify
# импортируем объект приложения
from . import app
# импортируем модель
from .models import URLMap
from .error_handlers import InvalidAPIUsage


# метод для преобразования сложных данных(экземпляра модели)
# в словарь
# по сути этот метод выполняет сериализацию данных
def to_dict(url_obj):
    return dict(
        id=url_obj.id,
        original=url_obj.original,
        short=url_obj.short,
        timestamp=url_obj.timestamp
    )


# явно разрешим метод GET
# создаем первую функцию get_url(id):
@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    # из GET-запроса получаем короткий идентификатор - short_id
    # запрашиваем объект модели URLMap по полученному short_id
    # в итоге поллучаем объект модели или ошибку 404
    url_map_obj = URLMap.query.filter_by(short=short_id).first_or_404()
    if url_map_obj is not None:
        # raise InvalidAPIUsage('В базе данных нет такой ссылки', 404)
        original_link = url_map_obj.original
    # а уже потом передаем этот словарь в качестве значения словаря в метод
    # jsonify, конвертируем данные в JSON
        return jsonify({'url': original_link}), 200
    raise InvalidAPIUsage('В базе данных нет такой ссылки', 404)
