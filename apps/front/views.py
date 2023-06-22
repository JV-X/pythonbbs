from flask import Blueprint, request, render_template, current_app, make_response, session, redirect, g
import string
import random
import time
from exts import cache, db
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO
from .forms import RegisterForm, LoginForm
from models.auth import UserModel
from .decorators import login_required
bp = Blueprint('front', __name__, url_prefix='/')


@bp.get('/')
def index():
    return render_template('front/index.html')


@bp.route('logout')
def logout():
    session.clear()
    return redirect('/')


@bp.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)


@bp.context_processor
def front_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


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
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error('没有这个用户')
            if not user.check_password(password):
                return restful.params_error('密码错误')
            session['user_id'] = user.id
            session.permanent = (remember == 1)
            return restful.ok()
        else:
            return restful.params_error(message=form.messages[0])


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
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.route('setting')
@login_required
def setting():
    return render_template('front/setting.html')
