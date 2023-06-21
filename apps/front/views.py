from flask import Blueprint, request, render_template, jsonify, current_app
import string
import random
from flask_mail import Message
from exts import mail, cache

bp = Blueprint('front', __name__, url_prefix='/')


# @bp.get('/email/captcha')
# def email_captcha():
#     email = request.args.get('email')
#     if not email:
#         return jsonify({'code': 400, 'message': '请传入邮箱'})
#     source = list(string.digits)
#     captcha = ''.join(random.sample(source, 6))
#     message = Message(subject='知了邮箱验证码', recipients=[email], body=f'您的验证码是{captcha}')
#     try:
#         mail.send(message)
#     except Exception as e:
#         print(e)
#         return jsonify({'code': 500, 'message': '邮件发送失败'})
#     return jsonify({'code': 200, 'message': '邮件发送成功'})
#

@bp.get('/email/captcha')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return jsonify({'code': 400, 'message': '请传入邮箱'})
    source = list(string.digits)
    captcha = ''.join(random.sample(source, 6))
    current_app.celery.send_task('send_mail', (email, '知了邮箱验证码', f'您的验证码是{captcha}'))
    cache.set(email, captcha)
    print(cache.get(email))
    return jsonify({'code': 200, 'message': '邮件发送成功'})


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
