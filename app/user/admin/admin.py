from flask import redirect, url_for, abort
from flask_admin.contrib.sqla import ModelView
from app.models import db
from app.user.user_model import User
from flask_admin import Admin, AdminIndexView
from flask_user import current_user

class AdminModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        if isinstance(current_user._get_current_object(), User):
            return current_user.has_roles(["Admin", ])

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)

class IndexView(AdminIndexView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        if isinstance(current_user._get_current_object(), User):
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return abort(403)

admin = Admin(name="Main", template_mode='bootstrap4', index_view=IndexView())
admin.add_view(AdminModelView(User, db.session, name="Users"))
