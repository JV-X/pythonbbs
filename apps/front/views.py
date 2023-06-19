from flask import Blueprint, request, render_template

bp = Blueprint('front', __name__, url_prefix='/')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('front/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('front/register.html')
