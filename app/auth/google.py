import datetime

from flask import flash, url_for, redirect
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound

from app.models.user import User, OAuth, Role
from app.database import db

google_blueprint = make_google_blueprint(
    scope=["openid",
           "https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user))


@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(bp, token):
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if not token:
        flash("Google-ით ავტორიზაციის დროს დაფიქსირდა შეცდომა", "danger")
        return redirect(url_for('auth.login'))

    resp = bp.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Google ანგარიშიდან მონაცემების მიღების დროს დაფიქსირდა შეცდომა", "danger")
        return redirect(url_for('auth.login'))

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    query = OAuth.query.filter_by(provider=bp.name, provider_user_id=google_user_id)

    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = str(google_info['email'])
        google_user_name = str(google_info['name'])
        google_user_first_name = str(google_info['given_name'])
        google_user_last_name = str(google_info['family_name'])
        oauth = OAuth(provider=bp.name,
                      provider_user_id=google_user_id,
                      provider_user_name=google_user_name,
                      provider_user_login=google_user_login,
                      provider_user_first_name=google_user_first_name,
                      provider_user_last_name=google_user_last_name,
                      token=token)

    if current_user.is_anonymous:
        if oauth.user:
            login_user(oauth.user)
            flash("Google-ით ავტორიზაცია წარმატებით დასრულდა", 'success')
            return redirect(url_for('files.all_files'))
        else:
            user = User(email=google_info['email'],
                        first_name=google_info['given_name'],
                        last_name=google_info['family_name'],
                        password=token['access_token'],
                        email_activation_key=None,
                        register_date=datetime.datetime.utcnow(),
                        confirmed_at=datetime.datetime.utcnow(),
                        active=1,
                        is_oauth=1
                        )
            user.roles.append(Role.query.filter_by(name='user').first())
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)

            flash("Google-ით ავტორიზაცია წარმატებით დასრულდა", 'success')
            return redirect(url_for('files.all_files'))


@oauth_error.connect_via(google_blueprint)
def google_error(bp, message, response):
    msg = '{name} OAuth-ის შეცდომა: "message={message} response={response}'.format(name=bp.name, message=message,
                                                                                   response=response)
    flash(msg, "danger")
