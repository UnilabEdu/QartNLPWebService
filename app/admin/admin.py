from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from app.database import db
from app.models.file import File, Pages, Sentences, Words, Statistics, Status
from app.models.ner_tagging import NerTags, NerTagType
from app.models.user import User, Role, OAuth
from flask_admin import Admin, AdminIndexView
from flask_login import current_user


class AdminModelView(ModelView):
    column_exclude_list = ['_password']

    def is_accessible(self):
        if isinstance(current_user, User):
            print(current_user.is_admin())
            return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class IndexView(AdminIndexView):
    column_exclude_list = ['_password']

    def is_accessible(self):
        if isinstance(current_user, User):
            return current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class UserView(AdminModelView):
    form_excluded_columns = ['oauth']


admin = Admin(name="Main", template_mode='bootstrap4', index_view=IndexView())
# User
admin.add_view(UserView(User, db.session, name="Users"))
admin.add_view(AdminModelView(Role, db.session, name="Roles"))
admin.add_view(AdminModelView(OAuth, db.session, name="OAuth Users"))
# Ner-tagging
admin.add_view(AdminModelView(NerTagType, db.session, name="Ner Tag Types"))
admin.add_view(AdminModelView(NerTags, db.session, name="Ner Tag Types to Words"))

# Files, words...
admin.add_view(AdminModelView(File, db.session, name="Files"))
admin.add_view(AdminModelView(Pages, db.session, name="Pages"))
admin.add_view(AdminModelView(Sentences, db.session, name="Sentences"))
admin.add_view(AdminModelView(Words, db.session, name="Words"))
admin.add_view(AdminModelView(Statistics, db.session, name="Statistics"))
admin.add_view(AdminModelView(Status, db.session, name="Statuses"))
