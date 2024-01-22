from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    message = "Пароль должен быть от 4 до 100 символов"
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                        Length(min=4, max=100, message=message)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    message_name = "Имя должно быть от 4 до 100 символов"
    message_psw = "Пароль должен быть от 4 до 100 символов"
    message_psw2 = "Пароли не совпадают"
    name = StringField("Имя: ", validators=[Length(min=4, max=100,
                                                   message=message_name)])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100,
                                                       message=message_psw)])
    psw2 = PasswordField("Повтор пароля: ",
                         validators=[DataRequired(),
                                     EqualTo('psw', message=message_psw2)])
    submit = SubmitField("Регистрация")
