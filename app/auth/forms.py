from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    email = StringField('', validators=[Required(), Length(1, 64),Email()])
    remember_me = BooleanField('Remember Me')
    password = PasswordField('', validators=[Required()])
    submit = SubmitField('Log in')
