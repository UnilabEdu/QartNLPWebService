from flask import flash
from flask_babel import gettext as _
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import ValidationError, HiddenField, BooleanField, StringField, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models.user import User


class LoginForm(FlaskForm):
    next = HiddenField()
    login = StringField(_('ელ-ფოსტა'), [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა'))])
    password = PasswordField(_('პაროლი'), [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი პაროლი'))])
    remember = BooleanField(_('დამიმახსოვრე'))
    submit_login = SubmitField(_('შესვლა'))


class SignupForm(FlaskForm):
    next = HiddenField()
    first_name = StringField(_('სახელი'),
                             [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი სახელი')),
                              Length(max=40,
                                     message=_('სახელი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან'))])
    last_name = StringField(_('გვარი'),
                            [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი გვარი')),
                             Length(max=40,
                                    message=_('გვარი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან'))])
    email = EmailField(_('ელ-ფოსტა'),
                       [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა')),
                        Email(message=_('ელ-ფოსტის მისამართი არასწორადაა შეყვანილი'))])
    password = PasswordField(_('პაროლი'),
                             [DataRequired(message=_('გთხოვთ შეიყვანოთ პაროლი')),
                              Length(min=6,
                                     max=128,
                                     message=_('პაროლი უნდა შედგებოდეს 6-128 სიმბოლოსგან'))])
    # EqualTo('confirm_password', message='შეყვანილი პაროლები არ ემთხვევა ერთმანეთს')])
    # confirm_password = PasswordField('გაიმეორეთ პაროლი',
    #                                  [DataRequired(message='გთხოვთ გაიმეოროთ არჩეული პაროლი')])
    submit_signup = SubmitField(_('რეგისტრაცია'))

    def validate_email(self, field):
        if User.select(email=field.data) is not None:
            raise ValidationError(_('შეყვანილი ელ-ფოსტა უკვე დაკავშირებულია სხვა ანგარიშთან'))


class ForgotPasswordForm(FlaskForm):
    email = EmailField(_('ელ-ფოსტა'),
                       [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა')),
                        Email(message=_('ელ-ფოსტის მისამართი არასწორადაა შეყვანილი'))])
    submit_password_forgot = SubmitField(_('პაროლის აღდგენა'))


class ResetPasswordForm(FlaskForm):
    password_reset_key = HiddenField()
    email = HiddenField()
    password = PasswordField(_('პაროლი'),
                             [DataRequired(message=_('გთხოვთ შეიყვანოთ პაროლი')),
                              Length(min=6,
                                     max=128,
                                     message=_('პაროლი უნდა შედგებოდეს 6-128 სიმბოლოსგან')),
                              EqualTo('confirm_password', message=_('შეყვანილი პაროლები არ ემთხვევა ერთმანეთს'))])
    confirm_password = PasswordField(_('გაიმეორეთ პაროლი'),
                                     [DataRequired(message=_('გთხოვთ გაიმეოროთ არჩეული პაროლი'))])
    submit_password_reset = SubmitField(_('პაროლის შეცვლა'))


class ChangeProfileDataForm(FlaskForm):
    email = HiddenField()
    old_password = PasswordField(_('ძველი პაროლი'))
    new_password = PasswordField(_('ახალი პაროლი'),
                                 [EqualTo('confirm_password', message=_('შეყვანილი პაროლები არ ემთხვევა ერთმანეთს'))])
    confirm_password = PasswordField(_('გაიმეორეთ პაროლი'))
    submit_password_change = SubmitField(_('პაროლის შეცვლა'))

    new_email = EmailField(_('ელ-ფოსტა'),
                           [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა')),
                            Email(message=_('ელ-ფოსტის მისამართი არასწორადაა შეყვანილი'))])
    submit_email = SubmitField(_('ელ-ფოსტის შეცვლა'))

    first_name = StringField(_('სახელი'),
                             [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი სახელი')),
                              Length(max=40,
                                     message=_('სახელი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან'))])
    last_name = StringField(_('გვარი'),
                            [DataRequired(message=_('გთხოვთ შეიყვანოთ თქვენი გვარი')),
                             Length(max=40,
                                    message=_('გვარი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან'))])
    password = PasswordField(_('პაროლი'))
    submit_profile_changes = SubmitField(_('მონაცემების შეცვლა'))


class ProfilePictureForm(FlaskForm):
    picture = FileField(_('პროფილის სურათი'), validators=[
        FileRequired(message=_('პროფილის სურათის განახლებისთვის აირჩიეთ სურათი.')),
        FileAllowed(['jpg', 'jpe', 'jpeg', 'png'],
                    message=_('პროფილის სურათი არ განახლდა. გთხოვთ აირჩიოთ .jpg, .jpe, .jpeg ან .png ფორმატის სურათი'))
    ])
    submit_picture = SubmitField(_('სურათის განახლება'))


def validate_new_email(email):
    if User.select(email=email) is not None:
        flash(_('შეყვანილი ელ-ფოსტა უკვე დაკავშირებულია სხვა ანგარიშთან'))
        return False
    return True
