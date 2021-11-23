from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import ValidationError, HiddenField, BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.html5 import EmailField

from app.models.user import User


class LoginForm(FlaskForm):
    next = HiddenField()
    login = StringField('ელ-ფოსტა', [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა')])
    password = PasswordField('პაროლი', [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი პაროლი')])
    remember = BooleanField('დამიმახსოვრე')
    submit_login = SubmitField('შესვლა')


class SignupForm(FlaskForm):
    next = HiddenField()
    first_name = StringField('სახელი',
                             [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი სახელი'),
                              Length(max=40,
                                     message='სახელი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან')])
    last_name = StringField('გვარი',
                            [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი გვარი'),
                             Length(max=40,
                                    message='გვარი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან')])
    email = EmailField('ელ-ფოსტა',
                       [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა'),
                        Email(message='ელ-ფოსტის მისამართი არასწორადაა შეყვანილი')])
    password = PasswordField('პაროლი',
                             [DataRequired(message='გთხოვთ შეიყვანოთ პაროლი'),
                              Length(min=6,
                                     max=128,
                                     message='პაროლი უნდა შედგებოდეს 6-128 სიმბოლოსგან')])
    # EqualTo('confirm_password', message='შეყვანილი პაროლები არ ემთხვევა ერთმანეთს')])
    # confirm_password = PasswordField('გაიმეორეთ პაროლი',
    #                                  [DataRequired(message='გთხოვთ გაიმეოროთ არჩეული პაროლი')])
    submit_signup = SubmitField('რეგისტრაცია')

    def validate_email(self, field):
        if User.select(email=field.data) is not None:
            raise ValidationError('შეყვანილი ელ-ფოსტა უკვე დაკავშირებულია სხვა ანგარიშთან')


class ForgotPasswordForm(FlaskForm):
    email = EmailField('ელ-ფოსტა',
                       [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა'),
                        Email(message='ელ-ფოსტის მისამართი არასწორადაა შეყვანილი')])
    submit_password_forgot = SubmitField('პაროლის აღდგენა')


class ResetPasswordForm(FlaskForm):
    password_reset_key = HiddenField()
    email = HiddenField()
    password = PasswordField('პაროლი',
                             [DataRequired(message='გთხოვთ შეიყვანოთ პაროლი'),
                              Length(min=6,
                                     max=128,
                                     message='პაროლი უნდა შედგებოდეს 6-128 სიმბოლოსგან'),
                              EqualTo('confirm_password', message='შეყვანილი პაროლები არ ემთხვევა ერთმანეთს')])
    confirm_password = PasswordField('გაიმეორეთ პაროლი',
                                     [DataRequired(message='გთხოვთ გაიმეოროთ არჩეული პაროლი')])
    submit_password_reset = SubmitField('პაროლის შეცვლა')


class ChangeProfileDataForm(FlaskForm):
    email = HiddenField()
    old_password = PasswordField('ძველი პაროლი')
    new_password = PasswordField('ახალი პაროლი',
                                  [EqualTo('confirm_password', message='შეყვანილი პაროლები არ ემთხვევა ერთმანეთს')])
    confirm_password = PasswordField('გაიმეორეთ პაროლი')
    submit_password_change = SubmitField('პაროლის შეცვლა')

    new_email = EmailField('ელ-ფოსტა',
                           [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი ელ-ფოსტა'),
                            Email(message='ელ-ფოსტის მისამართი არასწორადაა შეყვანილი')])
    submit_email = SubmitField('ელ-ფოსტის შეცვლა')

    first_name = StringField('სახელი',
                             [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი სახელი'),
                              Length(max=40,
                                     message='სახელი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან')])
    last_name = StringField('გვარი',
                            [DataRequired(message='გთხოვთ შეიყვანოთ თქვენი გვარი'),
                             Length(max=40,
                                    message='გვარი არ უნდა შედგებოდეს 40-ზე მეტი სიმბოლოსგან')])
    password = PasswordField('პაროლი')
    submit_profile_changes = SubmitField('მონაცემების შეცვლა')

    def validate_new_email(self, field):
        if User.select(email=field.data) is not None:
            raise ValidationError('შეყვანილი ელ-ფოსტა უკვე დაკავშირებულია სხვა ანგარიშთან')


class ProfilePictureForm(FlaskForm):
    picture = FileField('პროფილის სურათი', validators=[
        FileRequired(message='პროფილის სურათის განახლებისთვის აირჩიეთ სურათი.'),
        FileAllowed(['jpg', 'jpe', 'jpeg', 'png'],
                    message='პროფილის სურათი არ განახლდა. გთხოვთ აირჩიოთ .jpg, .jpe, .jpeg ან .png ფორმატის სურათი')
    ])
    submit_picture = SubmitField('სურათის განახლება')
