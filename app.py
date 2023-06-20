from flask import Flask
from exts import db,mail
import config
from flask_migrate import Migrate
from models import auth
from apps.front import front_bp
from bbs_celery import make_celery

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

mycelery = make_celery(app)

app.register_blueprint(front_bp)

if __name__ == '__main__':
    app.run()
