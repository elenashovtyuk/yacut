from flask import render_template, jsonify
from . import app, db


# создаем кастомный класс исключения для того, чтобы
# реализовать для АПИ возможность возвращать при одном и том же коде
# ошибки разные сообщения
# то есть, в зависимости от ошибки можно будет выбросить это исключение
# указав соответствующее сообщение и статус-код выполнения запроса
class InvalidAPIUsage(Exception):
    # по умолчанию(если статус-код ответа АПИ не указан),
    # то вернется код 400
    status_code = 400
    # конструктор класса принимает на вход текст сообщения
    # и статус-код ошибки(необязательно)

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        # если статус-код ответа передан в инструктор
        # то этот код вернется в ответе
        if status_code is not None:
            self.status_code = status_code

    # для подготовки JSON-ответа используем метод to dict,
    # который будет сериализовать сообщения
    def to_dict(self):
        return dict(message=self.message)

# обработчик для исключения InvalidAPIUsage
# если возникнет исключение InvalidAPIUsage, то этот обработчик
# будет готовить ответ в нужном формате
# нам нужно,чтобы отвернулся в формате JSON
# для регистрации функции-обработчика используем декоратор
# @app.errorhandler.
@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


# добавим новую функцию, которая будет обрабатывать
# исключение '404: страница не найдена'
# для регистрации функции-обработчика используем декоратор
# @app.errorhandler
@app.errorhandler(404)
def page_not_found(error):
    # вкачестве ответа вернется собственный шаблон и код ошибки
    return render_template('404.html'), 404


# зарегистрируем еще один обработчик - функцию, которая будет
# обрабатывать исключение "500: внутренняя ошибка сервера"
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
