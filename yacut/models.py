from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # метод для преобразования сложных данных(экземпляра модели)
    # в словарь
    # по сути этот метод выполняет сериализацию данных
    def to_dict(self):
        """Метод-сериализатор."""
        return dict(
            url=self.original,
            # функция url_for - принимает на вход функцию и возвращает URLдля нее
            # т.о осуществляется переход на нужную страницу
            # параметр external=True говорит о том, что фласку нужно сформировать абсолютную,
            # а не относительную ссылку. К этой абсолютной ссылке добавляем короткий идентификатор
            custom_id=url_for(
                'main_view', _external=True) + self.short
        )

    # добавим в модель новый метод-десериализатор
    # на вход этот метод принимает словарь data, полученный
    # из JSON в запросе
    # его задача - добавить в пустой объект класса URLMap
    # значения полей, которые будут переданы в POST-запросе
    def from_dict(self, data):
        """Метод-десериализатор."""
        for field_key, field_item in {'original': 'url', 'short': 'custom_id'}.items():
            # для каждой пары ключ:значение выполняем проверку
            # есть ли значение в data
            if field_item in data:
                setattr(self, field_key, data[field_item])
