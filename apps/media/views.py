from flask import Blueprint,send_from_directory,current_app

bp = Blueprint('media',__name__,url_prefix="/media")

@bp.route('avatar/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)
