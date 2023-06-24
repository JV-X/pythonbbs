import os
from datetime import timedelta

SECRET_KEY = 'asqwfrjvk689wk'

BASE_DIR = os.path.dirname(__file__)

DB_USERNAME = 'root'
DB_PASSWORD = 'xjv123..'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'pythonbbs'

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "xjv1195275315@qq.com"
MAIL_PASSWORD = "igtqeblbgaqyhgag"
MAIL_DEFAULT_SENDER = "xjv1195275315@qq.com"

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

CACHE_TYPE = 'RedisCache'
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = '127.0.0.1'
CACHE_REDIS_PORT = 6379

PERMANENT_SESSION_LIFETIME = timedelta(days=7)

AVATARS_SAVE_PATH = os.path.join(BASE_DIR, 'media', 'avatars')
POST_IMAGE_SAVE_PATH = os.path.join(BASE_DIR, 'media', 'post')

PER_PAGE_COUNT = 10
