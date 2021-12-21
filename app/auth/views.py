import datetime

from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_babel import gettext as _
from flask_login import login_required, logout_user, current_user
from flask_mail import Message
from itsdangerous import URLSafeSerializer

from app.auth.forms import ResetPasswordForm
from app.database import db
from app.extensions import mail
from app.models.user import User
from app.settings import Config

auth_blueprint = Blueprint('auth',
                           __name__,
                           template_folder='templates',
                           url_prefix='/')


@auth_blueprint.route('/resend_confirmation/<secretstring>')
def resend_email_confirmation(secretstring):
    s = URLSafeSerializer(Config.SECRET_KEY)
    user_email = s.loads(secretstring)[0]

    user = User.select(email=user_email)
    if not user.confirmed_at:
        flash(f'{_("ელ-ფოსტის ვერიფიკაციის შეტყობინება გაგზავნილია")} {user_email} {_("მისამართზე")}.', 'success')
        confirm_user_mail(user_email)
    else:
        flash(_('თქვენი ელ-ფოსტა უკვე ვერიფიცირებული იყო'), 'warning')

    return redirect(url_for('main.home-login'))


def confirm_user_mail(email):
    s = URLSafeSerializer(Config.SECRET_KEY)
    key = s.dumps([email])

    with current_app.app_context():
        target_user = User.select(email=email)
        target_user.email_activation_key = key
        db.session.commit()

    subject = _('QartNLP - ელ-ფოსტის ვერიფიკაცია')
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
        flash(_('ელ-ფოსტის ვერიფიკაცია წარმატებით დასრულდა!'), 'success')
    else:
        flash(_('თქვენი ელ-ფოსტა უკვე ვერიფიცირებული იყო'), 'warning')
    if current_user.is_authenticated:
        return redirect(url_for('files.all_files'))
    return redirect(url_for('main.home-login'))


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('თქვენ გამოხვედით სისტემიდან'), 'success')
    return redirect(url_for('main.home-login'))


@auth_blueprint.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('files.all_files'))

    form = ResetPasswordForm(password_reset_key=request.values["password_reset_key"],
                             email=request.values["email"])

    if form.validate_on_submit():
        result = update_password(form.email.data, form.password_reset_key.data, form.password.data)
        if result:
            flash(_('თქვენი პაროლი შეიცვალა'), 'success')
        else:
            flash(_('პაროლის აღდგენის ბმული მცდარია'), 'danger')

        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('main.home-login'))

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
    message = Message(subject=subject, html=html, recipients=[send_to], sender="QartNLP")
    mail.send(message)
