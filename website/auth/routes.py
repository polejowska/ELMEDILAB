from flask import render_template, redirect, url_for, session, flash, Blueprint
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from website.admin.utils import admin_access_required

from website.auth.forms import RequestForm, LoginForm
from website.models import ACCESS, Request, User
from website import bcrypt


auth = Blueprint("auth", __name__)


@auth.route("/request-access", methods=["GET", "POST"])
def new_user_form():
    """The route dedicated for request form.

    Returns:
        Renders template with the user request form or redirects to the main panel.
    """
    if current_user.is_authenticated:
        if current_user.status == ACCESS['admin']:
            return redirect(url_for("admin.admin_main"))
        return redirect(url_for("user.user_main"))
    request_form = RequestForm()
    request = None
    if request_form.validate_on_submit():
        request = Request.query.filter_by(email=request_form.email.data).first()
        if request is None:
            request = Request.create(
                username=request_form.username.data,
                email=request_form.email.data,
                password=request_form.password.data,
                country=request_form.country.data,
                profession=request_form.profession.data,
                education=request_form.education.data,
                additional_details=request_form.additional_details.data,
            )
            flash("Request sent successfully", "success")
        else:
            flash("Request cannot be sent", "danger")
        request_form.username.data = ""
        request_form.email.data = ""
    return render_template("user-request-access.html", form=request_form)


@auth.route("/login", methods=["GET", "POST"])
def index():
    """The route for logging in.

    Returns:
        Renders a login page or redirects to the main panel if the user is already logged in.
    """
    if current_user.is_authenticated:
        session["user"] = current_user.username
        return redirect(url_for("user.user_main", username=current_user.username))
    login_form = LoginForm()
    user = None
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.access == ACCESS["admin"]:
            login_user(user, remember=True)
            return redirect(url_for("admin.admin_main"))
        if user and bcrypt.check_password_hash(
            user.password, login_form.password.data
        ):
            login_user(user, remember=True)
            if current_user.access == ACCESS["admin"]:
                return redirect(url_for("admin.admin_main"))
            return redirect(url_for("user.user_main", username=user.username))

        login_form.email.data = ""
        login_form.username.data = ""
        login_form.password.data = ""
        flash(
            "Access denied. Please ensure the input data is correct or request access for an account.",
            "danger"
        )
    return render_template("login.html", form=login_form)


@auth.route("/logout")
@login_required
def logout():
    """The route for logging out.

    Returns:
        Logs out the user and redirects to the login page.
    """
    logout_user()
    session.pop("user", None)
    return redirect(url_for("auth.index"))
