from app.database import db
from app.models.user import User, Role
from app.models.file import File, Pages, Sentences, Words, Statistics, Status
from datetime import datetime
from werkzeug.security import generate_password_hash


def reset_db():
    db.drop_all()
    db.create_all()
    populate_db()


def populate_db():  # TODO: update db_reset command
    super_admin_role = find_or_create_role("super_admin")
    admin_role = find_or_create_role("admin")
    user_role = find_or_create_role("user")

    find_or_create_user(password=generate_password_hash('password'),
                        email='main_admin@mail.com',
                        role=admin_role)

    find_or_create_user(password=generate_password_hash('password'),
                        email='admin@mail.com',
                        role=super_admin_role)

    db.session.commit()


def find_or_create_role(name):
    role = Role.query.filter_by(name=name).first()

    if not role:
        role = Role(name)

        db.session.add(role)

    return role


def find_or_create_user(password, email, role=None):
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(email=email,
                    first_name='FirstName',
                    last_name='LastName',
                    _password=password,
                    confirmed_at=None,
                    active=True)

        if role:
            user.roles.append(role)

        db.session.add(user)

    return user


def clear_file_tables():
    db.session.query(File).delete()
    db.session.query(Pages).delete()
    db.session.query(Sentences).delete()
    db.session.query(Words).delete()
    db.session.query(Status).delete()
    db.session.query(Statistics).delete()
    db.session.commit()
