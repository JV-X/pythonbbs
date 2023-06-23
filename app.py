from flask import Flask
from exts import db, mail, cache, csrf,avatars
import config
from flask_migrate import Migrate
from models import auth
from apps.front import front_bp
from apps.media import media_bp
from bbs_celery import make_celery
import commands

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)

migrate = Migrate(app, db)

mycelery = make_celery(app)

app.register_blueprint(front_bp)
app.register_blueprint(media_bp)
app.cli.command('init_board')(commands.init_board)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
