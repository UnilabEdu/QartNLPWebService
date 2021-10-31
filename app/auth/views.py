import datetime
from uuid import uuid4

from app.extensions import mail
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, Markup
from flask_login import login_required, logout_user, current_user, login_user
from flask_mail import Message
from itsdangerous import URLSafeSerializer

from app.auth.forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm
from app.database import db
from app.models.user import User, Role
from app.settings import Config

auth_blueprint = Blueprint('auth',
                           __name__,
                           template_folder='templates',
                           url_prefix='/')


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('files.all_files'))

    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data, form.password.data)

        if user and authenticated:
            remember = request.form.get('remember') == 'y'

            if login_user(user, remember=remember):
                flash('თქვენ გაიარეთ ავტორიზაცია', 'success')

            return redirect(form.next.data or url_for('files.all_files'))

        elif user:
            flash('პაროლი არასწორია', 'danger')

        else:
            flash('მომხმარებელი ამ ელ-ფოსტით ვერ მოიძებნა', 'danger')

    elif request.method == 'POST':
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('files.all_files'))

    form = SignupForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        user.roles.append(Role.query.filter_by(name='user').first())
        form.populate_obj(user)
        user.register_date = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()

        confirm_user_mail(form.email.data)

        # Generate email resend hyperlink
        s = URLSafeSerializer(Config.SECRET_KEY)
        key = s.dumps([form.email.data])
        url = url_for('auth.resend_email_confirmation', secretstring=key)
        flash('რეგისტრაცია წარმატებით დასრულდა. '
              f'ელ-ფოსტის ვერიფიკაციის შეტყობინება გაგზავნილია {form.email.data} მისამართზე. \n' +
              Markup(f'<a href="{url}"> ვერიფიკაციის შეტყობინების ხელახლა გამოგზავნა </a>'), 'success')

        return redirect(url_for('auth.login'))

    elif request.method == 'POST':
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return render_template('auth/register.html', form=form)


@auth_blueprint.route('/resend_confirmation/<secretstring>')
def resend_email_confirmation(secretstring):
    s = URLSafeSerializer(Config.SECRET_KEY)
    user_email = s.loads(secretstring)[0]

    user = User.select(email=user_email)
    if not user.confirmed_at:
        flash(f'ელ-ფოსტის ვერიფიკაციის შეტყობინება გაგზავნილია {user_email} მისამართზე.', 'success')
        confirm_user_mail(user_email)
    else:
        flash('თქვენი ელ-ფოსტა უკვე ვერიფიცირებული იყო', 'warning')

    return redirect(url_for('auth.login'))


def confirm_user_mail(email):
    s = URLSafeSerializer(Config.SECRET_KEY)
    key = s.dumps([email])

    with current_app.app_context():
        target_user = User.select(email=email)
        target_user.email_activation_key = key
        db.session.commit()

    subject = 'QartNLP - ელ-ფოსტის ვერიფიკაცია'
    url = url_for('auth.confirm_account', secretstring=key, _external=True)
    html = render_template('emails/_confirm_account.html', project='QartNLP', url=url)

    send_async_email(subject, html, email)


@auth_blueprint.route('/confirm_account/<secretstring>', methods=['GET', 'POST'])
def confirm_account(secretstring):
    s = URLSafeSerializer(Config.SECRET_KEY)
    user_email = s.loads(secretstring)[0]
    user = User.select(email=user_email)
    if not user.confirmed_at:
        user.confirmed_at = datetime.datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        flash('ელ-ფოსტის ვერიფიკაცია წარმატებით დასრულდა!', 'success')
    else:
        flash('თქვენი ელ-ფოსტა უკვე ვერიფიცირებული იყო', 'warning')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('თქვენ გამოხვედით სისტემიდან', 'success')
    return redirect(url_for('auth.login'))


@auth_blueprint.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    form = ForgotPasswordForm()

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

            flash(f'პაროლის აღდგენის ინსტრუქცია გამოგზავნილია {user.email} მისამართზე.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(f'{form.email.data} მისამართით მომხმარებელი არ მოიძებნა.', 'danger')

    elif request.method == 'POST':
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return render_template('auth/forgot_password.html', form=form)


@auth_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('files.all_files'))

    form = ResetPasswordForm(password_reset_key=request.values["password_reset_key"],
                             email=request.values["email"])

    if form.validate_on_submit():
        result = update_password(form.email.data, form.password_reset_key.data, form.password.data)
        if result:
            flash('თქვენი პაროლი შეიცვალა', 'success')
        else:
            flash('პაროლის აღდგენის ბმული მცდარია', 'danger')

        return redirect(url_for('auth.login'))

    elif request.method == 'POST':
        for error in [*form.errors.values()]:
            flash(error[0], 'danger')

    return render_template('auth/reset_password.html', form=form)


def update_password(email, password_reset_key, password):
    user = User.select(email=email, password_reset_key=password_reset_key)
    if user:
        user.password = password
        user.password_reset_key = None
        db.session.commit()
        return True

    return False


def send_async_email(subject, html, send_to):
    message = Message(subject=subject, html=html, recipients=[send_to], sender="AnimaCore")
    mail.send(message)
