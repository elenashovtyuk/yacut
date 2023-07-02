from flask import render_template, jsonify
from . import app, db


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод-сериализатор."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """
    Функция-обработчик кастомного исключения InvalidAPIUsage.
    Для API.
    """
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """
    Функция-обработчик исключения 404 Not Found.
    Для пользовательского интерфейса.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Функция-обработчик исключения 500 Internal Server Error.
    Для пользовательского интерфейса.
    """
    db.session.rollback()
    return render_template('500.html'), 500
