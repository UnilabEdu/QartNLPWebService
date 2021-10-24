from app.database import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')

    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    profile = db.relationship('Profile', backref='user', uselist=False)
    file = db.relationship('File', backref='user')


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    date_of_birth = db.Column(db.DATE, nullable=False)
    img_url = db.Column(db.String)
    comp_name = db.Column(db.String(64))
    web_page = db.Column(db.String(64))
    info = db.Column(db.Text)

    def __init__(self, first_name, last_name, date_of_birth, img_url, comp_name, web_page, info):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.img_url = img_url
        self.comp_name = comp_name
        self.web_page = web_page
        self.info = info
