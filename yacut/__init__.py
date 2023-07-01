# этот файл __init__.py объединяет все файлы, все модули в пакет
# и этот пакет и будет представлять наше приложение

# что должно быть в этом файле:
# 1. подключение настроек
# 2. создание экземпляра класса Flask - экземпляра приложения
# 3. создание экземпляра БД

from flask import Flask

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from settings import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


from . import api_views, error_handlers, views, forms, models
