from wtforms import Form
from wtforms.validators import Email, Length, EqualTo, ValidationError
from wtforms.fields import StringField, IntegerField
from models.auth import UserModel
from exts import cache
from flask import request


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.append(errors)
        return message_list


class RegisterForm(BaseForm):
    email = StringField(validators=[Email(message='请传入邮箱')])
    email_captcha = StringField(validators=[Length(6, 6, message='请输入正确格式的邮箱验证码')])
    username = StringField(validators=[Length(3, 20, message='请输入正确格式的用户名')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    repeat_password = StringField(validators=[EqualTo('password', message='两次密码不一致')])
    graph_captcha = StringField(validators=[Length(4, 4, message='请输入正确格式的图形验证码')])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise ValidationError("邮箱已注册")

    def validate_email_captcha(self, field):
        email_captcha = field.data
        email = self.email.data
        cached_captcha = cache.get(email)
        if not email_captcha or email_captcha != cached_captcha:
            raise ValidationError('验证码错误')

    def validate_graph_captcha(self, field):
        graph_captcha = field.data
        key = request.cookies.get('_graph_captcha_key')
        cached_captcha = cache.get(key)
        if not cached_captcha or cached_captcha.lower() != graph_captcha.lower():
            raise ValidationError('图形验证码错误')


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请传入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()
