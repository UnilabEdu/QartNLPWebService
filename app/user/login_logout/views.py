from flask import Blueprint, render_template, redirect, url_for
from flask_user import login_required

login_logout_blueprint = Blueprint("login_logout",
                                   __name__,
                                   template_folder="templates/flask_user")

@login_logout_blueprint.route("user/sign-in", methods = ["GET", "POST"])
def login():
    pass

    # return redirect(url_for("user.login"))

@login_logout_blueprint.route("user/sign-out", methods = ["GET", "POST"])
@login_required
def logout():
    pass

    # return redirect(url_for("login_logout.login"))