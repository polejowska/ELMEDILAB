from flask import render_template, redirect, url_for, Blueprint
from flask_login.utils import login_required


main = Blueprint("main", __name__)


@main.route("/")
def base():
    """The route for redirecting to the login page."""
    return redirect(url_for("auth.index"))


@main.route("/help")
@login_required
def help():
    """The route for rendering help page template."""
    return render_template("help.html")


@main.route("/about")
@login_required
def about():
    """The route for rendering about page template."""
    return render_template("about.html")
