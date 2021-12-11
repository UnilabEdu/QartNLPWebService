from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm.collections import attribute_mapped_collection
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    picture = db.Column(db.String(), nullable=True)
    _password = db.Column(db.String(255), nullable=False)
    password_reset_key = db.Column(db.String(), nullable=True)
    email_activation_key = db.Column(db.String(), nullable=True)
    register_date = db.Column(db.DateTime())
    confirmed_at = db.Column(db.DateTime())
    is_oauth = db.Column(db.Boolean(), server_default='0')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    roles = db.relationship('Role', secondary='user_to_role',
                            backref=db.backref('user', lazy='dynamic'))
    file = db.relationship('File', backref='user', order_by='File.id')

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.select(email=email)

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    @classmethod
    def select(cls, email=None, password_reset_key=None):
        if password_reset_key and email:
            return cls.query.filter(func.lower(cls.email) == func.lower(email),
                                    cls.password_reset_key == password_reset_key).first()
        elif email:
            print(email)
            return cls.query.filter(func.lower(cls.email) == func.lower(email)).first()

    def is_admin(self):
        admin_role = Role.query.filter_by(name='admin').first()
        super_admin_role = Role.query.filter_by(name='super_admin').first()
        if admin_role in self.roles or super_admin_role in self.roles:
            return True
        else:
            return False

    def is_super_admin(self):
        super_admin_role = Role.query.filter_by(name='super_admin')
        if super_admin_role in self.roles:
            return True
        else:
            return False


class Role(db.Model):

    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


class UserRoles(db.Model):

    __tablename__ = 'user_to_role'

    id = db.Column(db.Integer(), primary_key=True)
    users_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    roles_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __init__(self, users_id, roles_id):
        self.users_id = users_id
        self.roles_id = roles_id


class OAuth(OAuthConsumerMixin, db.Model):

    __table_args__ = (db.UniqueConstraint("provider", "provider_user_id"),)

    provider_user_id = db.Column(db.String(256), nullable=False)
    provider_user_name = db.Column(db.String(256), nullable=False)
    provider_user_login = db.Column(db.String(256), nullable=False)
    provider_user_first_name = db.Column(db.String(256), nullable=False)
    provider_user_last_name = db.Column(db.String(256), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User, backref=db.backref("oauth", collection_class=attribute_mapped_collection("provider"),
                                                    cascade="all, delete-orphan",),)
