"""The routes.py file for routing related to a task."""

import os
from PIL import Image
from flask_login.utils import login_required
from werkzeug.utils import secure_filename

from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import current_user

from website.admin.utils import admin_access_required
from website.task.forms import CreateTaskForm, TaskForm
from website.models import (
    FILE_STATUS,
    DefaultLabel,
    Task,
    TaskDefaultLabel,
    Upload,
    TaskUpload,
)
from website.task.utils import (
    add_new_files,
    check_extension,
    add_default_label,
    get_items_names,
    make_directories,
    process_save_dicom_file,
    process_save_seq_file,
    process_save_video_file,
    remove_db_task_data,
    remove_directory,
)
from website import db


task = Blueprint("task", __name__)


DIRECTORY_TASKS = os.path.abspath("website\\LABEL\\TASKS\\")


@task.route("/admin/manage-tasks", methods=["GET", "POST"])
@login_required
@admin_access_required()
def manage_tasks():
    """The route for managing tasks.

    Returns:
        Renders the template with available tasks and tools for managing or redirects to the route for creating a new task.
    """
    tasks = Task.query.order_by(Task.id)
    task_upload = TaskUpload.query.order_by(TaskUpload.id)
    create_task_form = CreateTaskForm()
    if request.method == "POST":
        tasks_num = len(Task.query.all())
        return redirect(url_for("task.create_task", id=tasks_num + 1))
    return render_template(
        "admin-manage-tasks.html",
        form=create_task_form,
        tasks=tasks,
        task_upload=task_upload
    )


@task.route("/admin/cancel-task/<int:id>", methods=["GET", "POST"])
@login_required
@admin_access_required()
def cancel_task(id):
    """The route for cancelling the specified task. The task is not submitted and not visible on the tasks list.

    Args:
        id (int): The unique task identifier.
    """
    remove_directory(os.path.abspath(DIRECTORY_TASKS + "\\" + str(id)))
    remove_db_task_data(task_id=id)
    return redirect(url_for("task.manage_tasks"))


@task.route("/admin/create-task/<int:id>", methods=["GET", "POST"])
@login_required
@admin_access_required()
def create_task(id):
    """The rout for creating a new task. When submitted, will be visible on the task list and available for users.

    Args:
        id (int): The unique identifier for the newly created task.

    Returns:
        Renders a template with the task's data form or redirects to the tasks list.
    """
    dir_files = os.path.abspath(DIRECTORY_TASKS + "\\" + str(id) + "\\FILES")
    dir_labels = os.path.abspath(DIRECTORY_TASKS + "\\" + str(id) + "\\ANNOTATIONS\\")
    make_directories(dir_files, dir_labels)

    task_form = TaskForm()

    uploads_list = get_items_names(
        query=TaskUpload.query.filter(TaskUpload.task_id == id).all(), table=Upload
    )

    if task_form.validate_on_submit():
        if task_form.create.data:
            if not bool(uploads_list):
                flash("Please upload at least one file in order to create this task.", "warning")
                return redirect(url_for("task.create_task", id=id))
            if task_form.name.data is not None:
                Task.create(id=id, name=task_form.name.data)
            else:
                Task.create(id=id, name="Unnamed")
            return redirect(url_for("task.manage_tasks"))
        if task_form.upload.data:
            if "files[]" not in request.files:
                return redirect(request.url)
            files = request.files.getlist("files[]")
            for file in files:
                if file and check_extension(file.filename):
                    filename = secure_filename(file.filename)
                    extension = filename.rsplit(".", 1)[1].lower()
                    if extension == "seq":
                        camera = dict(task_form.select_camera.choices).get(
                            task_form.select_camera.data
                        )
                        frames = task_form.select_frames.data
                        if frames is None or frames == 0:
                            flash(
                                "Please enter the correct number of frames if a sequence is uploaded.",
                                "warning"
                            )
                            return redirect(url_for("task.create_task", id=id))
                        process_save_seq_file(file, dir_files, filename, camera, frames)
                        add_new_files(id, dir_files)
                    if extension == "mp4":
                        process_save_video_file(file, dir_files, filename, task_id=id)
                    if extension == "dcm":
                        process_save_dicom_file(file, dir_files, filename)
                    upload = Upload(
                        data=file.read(), mimetype=file.mimetype, name=filename
                    )
                    db.session.add(upload)
                    db.session.commit()
                    if upload.id is not None:
                        task_upload = TaskUpload(task_id=id, upload_id=upload.id)
                        db.session.add(task_upload)
                        db.session.commit()
                        if extension not in ("dcm", "mp4", "seq"):
                            img = Image.open(file.stream)
                            img.save(os.path.join(dir_files, filename))
                        if extension in ("mp4", "seq"):
                            os.remove(os.path.join(dir_files, filename))
                            db.session.delete(task_upload)
                            db.session.delete(upload)
                            db.session.commit()
                    flash(filename + " uploaded successfully", "success")
                else:
                    flash(
                        "The uploaded file is not supported."
                        + " Please upload new file with appropriate extension."
                        + " Supported files: 'png', 'jpg', 'jpeg', 'bmp', 'dcm', 'mp4', 'seq'.",
                        "danger",
                    )
                    return redirect(url_for("task.create_task", id=id))
        if task_form.add.data:
            if task_form.default_label.data is not None:
                add_default_label(
                    task_id=id, default_label=task_form.default_label.data
                )

    uploads_list = get_items_names(
        query=TaskUpload.query.filter(TaskUpload.task_id == id).all(), table=Upload
    )

    return render_template(
        "admin-create-task.html",
        id=id,
        form=task_form,
        uploads=uploads_list,
        default_labels=get_items_names(
            query=TaskDefaultLabel.query.filter(TaskDefaultLabel.task_id == id).all(),
            table=DefaultLabel
        ),
    )


@task.route("/task-details/<int:task_id>")
@login_required
@admin_access_required()
def check_task_details(task_id):
    """The route for page displaying files within a selected task.

    Args:
        task_id (int): The task's unique identifier.

    Returns:
        Returns a template with the task's data.
    """
    return render_template("task-details.html", task_id=task_id)


@task.route("/change-task-status/<int:task_id>/<int:status>")
@login_required
@admin_access_required()
def change_task_status(task_id, status):
    """The route for modifying the task's status (possible status: "open", "closed").

    Args:
        task_id (int): The task's unique identifier.
        status (int): THe task's status.

    Returns:
        Redirects to the page for managing tasks.
    """
    task = Task.query.filter(Task.id == task_id, Task.status == status).first()
    task.status ^= 1
    db.session.commit()
    return redirect(url_for("task.manage_tasks"))


@task.route("/change-file-status/<int:task_id>/<int:file_id>/<int:status>")
@login_required
@admin_access_required()
def change_file_status(task_id, file_id, status):
    """The route for modifying file status (possible status: "new", "in progress", "annotated", "closed").

    Args:
        task_id (int): The task's unique identifier.
        file_id (int): The file's unique identifier.
        status (int): The current status of the file within the task.

    Returns:
        Redirects to the files list within a selected task.
    """
    upload = Upload.query.filter(Upload.id == file_id).first()
    if upload.status <= 2:
        upload.status = FILE_STATUS["CLOSED"]
    else:
        upload.status = FILE_STATUS["NEW"]
    db.session.commit()
    return redirect(
        url_for("user.task_files", username=current_user.username, task_id=task_id)
    )


@task.route("/remove-task/<int:task_id>")
@login_required
@admin_access_required()
def remove_task(task_id):
    """The route for removing the task.

    Args:
        task_id (id): The task unique identifier.

    Returns:
        Redirects to the managing tasks section.
    """
    remove_db_task_data(task_id=task_id)
    remove_directory(os.path.abspath(DIRECTORY_TASKS + "\\" + str(task_id)))
    return redirect(url_for("task.manage_tasks"))
