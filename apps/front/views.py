from flask import Blueprint, request, render_template, current_app, make_response
import string
import random
import time
from exts import cache, db
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO
from .forms import RegisterForm
from models.auth import UserModel

bp = Blueprint('front', __name__, url_prefix='/')


@bp.get('graph/captcha')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    key = md5((captcha + str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key, captcha)

    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    resp.set_cookie('_graph_captcha_key', key, max_age=3600)
    return resp


@bp.get('/email/captcha')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error(message='请传入邮箱')
    source = list(string.digits)
    captcha = ''.join(random.sample(source, 6))
    current_app.celery.send_task('send_mail', (email, '知了邮箱验证码', f'您的验证码是{captcha}'))
    cache.set(email, captcha)
    print(cache.get(email))
    return restful.ok('邮件发送成功')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            u = UserModel(email=email, username=username, password=password)
            db.session.add(u)
            db.session.commit()
            return restful.ok()
        else:
            print(form.errors)
            return 'fail'
