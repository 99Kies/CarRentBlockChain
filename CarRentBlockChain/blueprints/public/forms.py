# -*- coding: utf-8 -*-
"""Public forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from CarRentBlockChain.blueprints.public.models import User


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()
        if not self.user:
            self.username.errors.append("Unknown username")
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append("Invalid password")
            return False

        if not self.user.active and not self.user.is_admin:
            self.username.errors.append("User not activated or not admin")
            return False
        return True

class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username", validators=[DataRequired('请选择标签'), Length(min=3, max=25)]
    )
    email = StringField(
        "Email", validators=[DataRequired('请选择标签'), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired('请选择标签'), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        "Verify password",
        [DataRequired('请选择标签'), EqualTo("password", message="Passwords must match")],
    )
    iphone = StringField(
        "iPhone Number", validators=[DataRequired('请选择标签'), Length(min=11, max=11)]
    )
    idcard = StringField(
        "ID Card", validators=[DataRequired('请选择标签'), Length(min=18, max=19)]
    )

    status = SelectField(
        label='身份（车主CarOwner/租车用户User）',
        validators=[DataRequired('请选择标签')],
        render_kw={
            'class': 'form-control'
        },
        choices=[(1, 'CarOwner'), (2, 'User')],
        default=2,
        coerce=int
    )
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True
