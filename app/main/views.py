from flask import Blueprint, render_template, request, flash, redirect, session
from flask_login import current_user

from app.auth.functions import get_auth_forms, login, register, forgot_password
from app.extensions import babel
from app.main.temp_data import people
from app.settings import Config

main_blueprint = Blueprint('main',
                           __name__,
                           url_prefix='/'
                           )


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


@main_blueprint.route('/', methods=['GET', 'POST'], endpoint='home')
@main_blueprint.route('/login', methods=['GET', 'POST'], endpoint='home-login')
@main_blueprint.route('/about_us', methods=['GET', 'POST'], endpoint='about')
@main_blueprint.route('/lemma', methods=['GET', 'POST'], endpoint='lemma')
def info_views():
    """
    Contains outer pages which don't require authorization and have auth popups: landing page, lemmatization, about us...
    """
    forms = None
    redirect_next = request.args.get('next')
    submitted_form = 'login' if redirect_next else None
    max_character_count = Config.DEMO_LEMMATIZATION_LIMIT
    if redirect_next and request.method == 'GET':
        flash('გთხოვთ გაიაროთ ავტორიზაცია', 'danger')
    elif request.endpoint == 'main.home-login':
        submitted_form = 'login'

    if not current_user.is_authenticated:
        forms = get_auth_forms()
        if forms['login'].submit_login.data:
            response_redirect = login(forms['login'], redirect_next)
            submitted_form = 'login'
            if response_redirect:
                return redirect(response_redirect)

        elif forms['signup'].submit_signup.data:
            response_redirect = register(forms['signup'], redirect_next)
            submitted_form = 'signup'
            if response_redirect:
                return redirect(response_redirect)

        elif forms['forgot'].submit_password_forgot.data:
            forgot_password(forms['forgot'])
            submitted_form = 'forgot'

    if request.endpoint == 'main.home' or request.endpoint == 'main.home-login':
        return render_template('main/main.html', forms=forms, submitted_form=submitted_form)
    elif request.endpoint == 'main.about':
        return render_template('main/about.html', forms=forms, submitted_form=submitted_form, people=people)
    elif request.endpoint == 'main.lemma':
        return render_template('main/lemma.html', forms=forms, submitted_form=submitted_form, max_character_count=max_character_count)
