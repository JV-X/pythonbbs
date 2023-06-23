from flask import Blueprint,send_from_directory,current_app

bp = Blueprint('media',__name__,url_prefix="/media")


@bp.route('avatar/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

@bp.route('post/<filename>')
def get_post_image(filename):
    return send_from_directory(current_app.config['POST_IMAGE_SAVE_PATH'],filename)
