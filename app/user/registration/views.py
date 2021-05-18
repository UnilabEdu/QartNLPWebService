from flask import Blueprint, redirect, url_for

registration_blueprint = Blueprint("register",
                                   __name__,
                                   template_folder="templates/flask_user")

@registration_blueprint.route("user/register", methods = ["GET", "POST"])
def register():
    pass

    # return redirect(url_for("user.register"))