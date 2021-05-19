from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from app.models import db
from app.user.user_model import User
from flask_admin import Admin, AdminIndexView
from flask_user import current_user

class AdminModelView(ModelView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login'))

class IndexView(AdminIndexView):
    column_exclude_list = ['password', ]

    def is_accessible(self):
        return current_user.has_role("Admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('user.login'))

admin = Admin(name="Main", template_mode='bootstrap4', index_view=IndexView())
admin.add_view(AdminModelView(User, db.sesion, name="Users"))
