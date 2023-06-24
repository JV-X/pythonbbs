from flask import (
    Blueprint,
    request,
    render_template,
    current_app,
    make_response,
    session,
    redirect,
    g,
    jsonify,
    url_for,
)
import string
import random
import time
from exts import cache, db
from utils import restful
from utils.captcha import Captcha
from hashlib import md5
from io import BytesIO
from .forms import RegisterForm, LoginForm, UploadImageForm, EditProfileForm, PublicPostForm, PublicCommentForm
from models.auth import UserModel
from .decorators import login_required
from flask_avatars import Identicon
import os
from models.post import BoardModel, BannerModel, PostModel, CommentModel
from flask_paginate import get_page_parameter, Pagination

bp = Blueprint('front', __name__, url_prefix='/')


@bp.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)


@bp.get('/')
def index():
    boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
    posts_query = PostModel.query.order_by(PostModel.create_time.desc())
    total = posts_query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * current_app.config['PER_PAGE_COUNT']
    end = start + current_app.config['PER_PAGE_COUNT']
    posts = posts_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, total=total)
    return render_template('front/index.html', boards=boards, posts=posts, pagination=pagination)


@bp.route('logout')
def logout():
    session.clear()
    return redirect('/')


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
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode('utf-8')).hexdigest())
            avatar = filenames[2]
            u = UserModel(email=email, username=username, password=password, avatar=avatar)
            db.session.add(u)
            db.session.commit()
            return restful.ok()
        else:
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.route('setting')
@login_required
def setting():
    email_hash = md5(g.user.email.encode('utf-8')).hexdigest()
    return render_template('front/setting.html', email_hash=email_hash)


@bp.post('avatar/upload')
@login_required
def upload_avatar():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode('utf-8')).hexdigest() + ext
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={'avatar': filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.post('profile/edit')
@login_required
def edit_profile():
    form = EditProfileForm(request.form)
    if form.validate():
        signature = form.signature.data
        g.user.signature = signature
        db.session.commit()
        return restful.ok(message='修改个人信息成功')
    else:
        return restful.params_error(message=form.messages[0])


@bp.route('/post/public', methods=['POST', 'GET'])
def public_post():
    if request.method == 'GET':
        boards = BoardModel.query.order_by(BoardModel.priority.desc()).all()
        return render_template('front/public_post.html', boards=boards)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            board_id = form.board_id.data
            content = form.content.data
            try:
                board = BoardModel.query.get(board_id)
            except Exception as e:
                return restful.params_error(message='版块不存在')
            post = PostModel(title=title, board=board, content=content, author=g.user)
            db.session.add(post)
            db.session.commit()
            return restful.ok('帖子创建成功')
        else:
            return restful.params_error(message=form.messages[0])


@bp.get('post/detail/<int:post_id>')
def post_detail(post_id):
    try:
        post = PostModel.query.get(post_id)
    except Exception as e:
        return 404
    comment_count = CommentModel.query.filter_by(post_id=post_id).count()
    context = {
        'comment_count': comment_count,
        'post': post,
    }
    return render_template('front/post_detail.html', **context)


@bp.post('/comment')
@login_required
def public_comment():
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        try:
            post = PostModel.query.get(post_id)
        except Exception as e:
            return restful.params_error(message='没有这篇帖子')
        comment = CommentModel(content=content)
        comment.author = g.user
        comment.post = post
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])


@bp.post('post/image/upload')
@login_required
def upload_post_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode('utf-8')).hexdigest() + ext
        image_path = os.path.join(current_app.config['POST_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)

        return jsonify({
            'errno': 0,
            'data': [{
                'url': url_for('media.get_post_image', filename=filename),
                'alt': filename,
                'href': '',
            }]
        })
    else:
        message = form.messages[0]
        return restful.params_error(message=message)
