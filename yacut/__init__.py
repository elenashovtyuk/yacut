# из модуля flask импортируем класс Flask -
# для создания приложения
from flask import Flask

# from flask_migrate import Migrate

# импортируется нужный класс для работы с ORM
from flask_sqlalchemy import SQLAlchemy

from settings import Config


# создаем объект приложения - экземпляр класса Flask
# единственный аргумент - это имя текущего модуля или пакета(yacut)
app = Flask(__name__)

app.config.from_object(Config)

# создаем экземпляр класса SQLAlchemy и передаем
# в качестве параметра экземпляр приложения Flask
db = SQLAlchemy(app)


from . import error_handlers, views
