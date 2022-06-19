"""Mapping the admin URLs to the code rendering the web page."""

import os

from flask import render_template, redirect, url_for, Blueprint
from flask_login.utils import login_required

from website.task.routes import DIRECTORY_TASKS
from website.task.utils import remove_directory
from website.admin.utils import (
    add_new_user,
    configure_db_records,
    admin_access_required,
    remove_existing_user,
    remove_new_request,
)
from website.models import Request, User
from website import db


admin = Blueprint("admin", __name__)



@admin.route("/admin")
@login_required
@admin_access_required()
def admin_main():
    """The route to admin main panel.

    Returns:
        Renders admin-main.html template.
    """
    return render_template("admin-main.html")


@admin.route("/admin/requests", methods=["GET", "POST"])
@admin_access_required()
def approve_requests():
    """The route for approving requests.

    Returns:
        Renders template with requests management panel.
    """
    requests = Request.query.order_by(Request.date_requested)
    return render_template("admin-approve-requests.html", requests=requests)


@admin.route("/add-user/<int:request_id>")
@admin_access_required()
def add_user(request_id):
    """The route for adding new user.

    Args:
        request_id (int): The request unique identifier.

    Returns:
        Redirects to requests list.
    """
    request_approved = Request.query.get(request_id)
    request_approved.approved = True
    add_new_user(request_approved)
    remove_new_request(request_id)

    return redirect(url_for("admin.approve_requests"))


@admin.route("/admin/users")
@admin_access_required()
def users():
    """The route for managing users.

    Returns:
        Renders a page with users list.
    """
    users = User.query.order_by(User.date_added)
    return render_template("admin-users.html", users=users)


@admin.route("/remove-request/<int:request_id>")
@admin_access_required()
def remove_request(request_id):
    """The route for removing the request.

    Args:
        request_id (int): The request's unique identifier.

    Returns:
        Redirects to modified requests list.
    """
    remove_new_request(request_id)
    return redirect(url_for("admin.approve_requests"))


@admin.route("/admin/remove/<int:user_id>")
@admin_access_required()
def remove_user(user_id):
    """The route for removing the user.

    Args:
        user_id (int): The user's unique identifier.

    Returns:
        Redirects to modified users list.
    """
    remove_existing_user(user_id)
    return redirect(url_for("admin.users"))


@admin.route("/admin/restart-db")
@admin_access_required()
def admin_restart_db():
    """The route for restarting the database.

    Returns:
        Renders admin main panel template.
    """
    db.drop_all()
    db.create_all()
    configure_db_records()
    remove_directory(os.path.abspath(DIRECTORY_TASKS))
    return render_template("admin-main.html")