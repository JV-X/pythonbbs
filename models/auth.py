from werkzeug.security import check_password_hash, generate_password_hash
from exts import db
import shortuuid
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(200), nullable=False)
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    join_time = db.Column(db.DateTime, default=datetime.now)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(UserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self.password, rawpwd)

    def has_permission(self, permission):
        # 当前用户所拥有的权限&permission = permission
        # 0b011 & 0b001 = 0b001
        # 0b011 & 0b100 = 0b000
        return (self.role.permissions & permission) == permission
