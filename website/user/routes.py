from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required

from website.models import FILE_STATUS, Annotation, Task, Upload, User
from website.user.utils import get_uploads_id
from website.user.forms import UpdateAccountForm
from website import db


user = Blueprint("user", __name__)


@user.route("/user-<string:username>")
@login_required
def user_main(username):
    """The route for main user panel.

    Args:
        username (str): The username.

    Returns:
        Renders a page with user panel displaying available options.
    """
    return render_template("user-main.html")


@user.route("/user-<string:username>/profile", methods=["GET", "POST"])
@login_required
def profile(username):
    """The route for user profile form.

    Args:
        username (str): The username.
    Returns:
        Renders a page with user profile.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.country = form.country.data
        current_user.education = form.education.data
        current_user.profession = form.profession.data
        current_user.additional_details = form.additional_details.data
        db.session.commit()
        flash("Changes have been saved successfully.", "success")
        return redirect(url_for("user.profile", username=username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.country.data = current_user.country
        form.education.data = current_user.education
        form.profession.data = current_user.profession
        form.additional_details.data = current_user.additional_details
    return render_template("user-profile.html", form=form)


@user.route("/user-<string:username>/tasks")
@login_required
def tasks(username):
    """The route for the list of tasks.

    Args:
        username (str): The username.

    Returns:
        Renders the template with tasks.
    """
    tasks = Task.query.order_by(Task.status.desc())
    return render_template("user-tasks.html", tasks=tasks, mode="closed")


@user.route("/user-<string:username>/task-<int:task_id>/files")
@login_required
def task_files(username, task_id):
    """"The route dedicated for files included in a task operations.

    Args:
        username (str): The username.
        task_id (int): The task unique identifier.

    Returns:
        Renders a page with files included in a chosen task.
    """
    task_status = Task.query.filter(Task.id == task_id).first().status
    if not task_status:
        return redirect(url_for("user.tasks", username=username))

    uploads_id = get_uploads_id(task_id)
    uploads_entries = []
    upload_annotations_num = {}
    for upload_id in uploads_id:
        upload = Upload.query.filter(Upload.id == upload_id).first()
        annotations_num = len(
            Annotation.query.filter_by(task_id=task_id, filename=upload.name).all()
        )
        upload_annotations_num[upload.name] = annotations_num
        if upload.status == FILE_STATUS["CLOSED"]:
            pass
        elif upload.status == FILE_STATUS["IN PROGRESS"]:
            pass
        else:
            if annotations_num == 0:
                upload.status = FILE_STATUS["NEW"]
            if annotations_num > 0:
                upload.status = FILE_STATUS["ANNOTATED"]
        uploads_entries.append(upload)
        db.session.commit()

    if current_user.access == 2:
        return render_template(
            "task-details.html",
            files=uploads_entries,
            task_id=task_id,
            upload_annotations_num=upload_annotations_num
        )

    return render_template(
        "task-files.html",
        files=uploads_entries,
        task_id=task_id,
        upload_annotations_num=upload_annotations_num,
    )


@user.route("/user-profile/<string:username>")
@login_required
def display_user_profile(username):
    """The route for the other than the current user user profile page.

    Args:
        username (str): The username of the user which profile is selected.

    Returns:
        Renders the page with the user profile.
    """
    user = User.query.filter_by(username=username).first()
    return render_template("user-profile-external.html", user=user, username=username)
