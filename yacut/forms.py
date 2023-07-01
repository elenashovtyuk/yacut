# добавляем необходимые импорты:
# из модуля flask_wtf импортируем класс FlaskForm
# Мы создаем форму, наследуясь от этого класса
from flask_wtf import FlaskForm

# типы полей формы и валидаторы импортируем из библиотеки WTForms
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import URL, DataRequired, Optional, Length, Regexp


# создаем форму, чтобы пользователь мог самостоятельно создать новый
# короткий вариант ссылки через эту форму
# у каждого поля этой формы есть как минимум заголовок и дополнительные аргументы
class URLMapForm(FlaskForm):
    # первое поле формы - поле для длинной оригинальной ссылки
    # это поле имеет тип текстовое поле для ввода URL-адреса
    # укажем для этого поля следующие аргументы:
    # название поля, которое отобразится внутри этого поля,
    # cписок валидаторов(DataRequired - проверяет, что пользователь ввел
    # хоть какие-то данные, так как поле обязательное
    # валидатор URL, проверяет URL-адрес,
    # Length - задает ограничение по длине)
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            URL(message='Введена некорректная ссылка'),
            Length(1, 256)
        ]
    )

    # второе поле формы - поле для пользовательского варианта короткого идентификатора
    # это поле также имеет строковый тип
    # укажем для этого поля следующие аргументы:
    # название поля, которое отобразится внутри этого поля,
    # список валидаторов(Optional - позволяет полю быть необязательным,
    # Length - пользовательский вариант короткой ссылки должен быть не больше 16 символов,
    # Regexp - проверяет соответствие определенной маске)
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(
                regex=r'^[a-zA-Z\d]{1,16}$',
                message='Недопустимые символы. Допустимы только буквы "a-Z" и цифры "0-9"')
        ]
    )

    # также необходимо добавить кнопку "Cоздать", при нажатии
    # на которую будет создан пользовательский вариант короткой сслыки
    submit = SubmitField('Создать')
