from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from website.models import Request, User


class RequestForm(FlaskForm):
    """The request form that user submits in order to acquire an account to gain access to the system.

    Raises:
        ValidationError: Raised when invalid username or email is entered.
    """
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=25)],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm password"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    education = StringField("Education", render_kw={"placeholder": "Education"})
    profession = StringField("Profession", render_kw={"placeholder": "Profession"})
    country = StringField("Country", render_kw={"placeholder": "Country"})
    additional_details = StringField(
        "Additional details", render_kw={"placeholder": "Additional details"}
    )
    submit = SubmitField("Send this request")

    def validate_username(self, username):
        request = Request.query.filter_by(username=username.data).first()
        user = User.query.filter_by(username=username.data).first()
        if request or user:
            raise ValidationError(
                "The specified username is already taken. Please input a unique username."
            )

    def validate_email(self, email):
        request = Request.query.filter_by(email=email.data).first()
        user = User.query.filter_by(email=email.data).first()
        if request or user:
            raise ValidationError("An account with the specified email already exists.")


class LoginForm(FlaskForm):
    """The login form where user enters data to access the pages for logged users.
    """
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    submit = SubmitField("Log in")
