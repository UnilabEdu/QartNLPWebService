import datetime
from uuid import uuid4

from flask import render_template, flash, url_for, Markup
from flask_login import login_user
from itsdangerous import URLSafeSerializer

from app.auth.forms import LoginForm, SignupForm, ForgotPasswordForm
from app.auth.views import confirm_user_mail, send_async_email
from app.database import db
from app.models.user import User, Role
from app.settings import Config


def get_auth_forms():
    return {
                'login': LoginForm(),
                'signup': SignupForm(),
                'forgot': ForgotPasswordForm()
            }


def login(form, redirect_next):
    redirect_string = None

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data, form.password.data)

        if user and authenticated:
            remember = form.remember

            if login_user(user, remember=remember):
                flash('თქვენ გაიარეთ ავტორიზაცია', 'success')
            redirect_string = redirect_next or url_for('files.all_files')

        elif user:
            flash('პაროლი არასწორია', 'danger')

        else:
            flash('მომხმარებელი ამ ელ-ფოსტით ვერ მოიძებნა', 'danger')

    else:
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return redirect_string or False


def register(form, redirect_next):
    redirect_string = None

    if form.validate_on_submit():
        user = User()
        user.roles.append(Role.query.filter_by(name='user').first())
        form.populate_obj(user)
        user.register_date = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.flush()
        registered_user_id = user.id
        db.session.commit()

        confirm_user_mail(form.email.data)

        # Generate email resend hyperlink
        s = URLSafeSerializer(Config.SECRET_KEY)
        key = s.dumps([form.email.data])
        url = url_for('auth.resend_email_confirmation', secretstring=key)
        flash('რეგისტრაცია წარმატებით დასრულდა. '
              f'ელ-ფოსტის ვერიფიკაციის შეტყობინება გაგზავნილია {form.email.data} მისამართზე. \n' +
              Markup(f'<a href="{url}"> ვერიფიკაციის შეტყობინების ხელახლა გამოგზავნა </a>'), 'success')

        login_user(User.query.get(registered_user_id), remember=True)

        redirect_string = redirect_next or url_for('files.all_files')

    else:
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return redirect_string or False


def forgot_password(form):
    if form.validate_on_submit():
        user = User.select(email=form.email.data)

        if user:
            user.password_reset_key = str(uuid4())
            db.session.commit()

            subject = 'QartNLP - პაროლის აღდგენა'
            url = url_for('auth.reset_password', email=user.email,
                          password_reset_key=user.password_reset_key, _external=True)
            html = render_template('emails/_reset_password.html', project='QartNLP', url=url)

            send_async_email(subject, html, user.email)

            flash(f'პაროლის აღდგენის ინსტრუქცია გამოგზავნილია!', 'success')
        else:
            flash(f'{form.email.data} მისამართით მომხმარებელი არ მოიძებნა.', 'danger')

    else:
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')
