from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from flask_login import current_user

from website.models import User


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=20)],
        render_kw={"placeholder": "Username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )
    profession = StringField("Profession", render_kw={"placeholder": "Profession"})
    country = StringField("Country", render_kw={"placeholder": "Country"})
    education = StringField("Education", render_kw={"placeholder": "Education"})
    profession = StringField("Profession", render_kw={"placeholder": "Profession"})
    additional_details = StringField(
        "Additional details", render_kw={"placeholder": "Additional details"}
    )
    submit = SubmitField("SAVE")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "The specified username is already taken. Please input a unique username."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "An account with the specified email already exists."
                )
