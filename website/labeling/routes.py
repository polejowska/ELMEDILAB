from flask import (
    render_template,
    redirect,
    url_for,
    send_file,
    request,
    Blueprint,
    current_app,
)
from flask_login.utils import login_required
from website.export_convert.utils import write_annotations

from website.models import FILE_STATUS, Annotation, TaskDefaultLabel, Upload
from website.labeling.utils import get_predefined_labels, get_saved_labels
from website import db

import os


labeling = Blueprint("labeling", __name__)


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/label/<string:mode>",
    methods=["GET", "POST"],
)
@login_required
def task_label(username, task_id, mode, file_id):
    """The route for managing mechanisms related to starting labeling the selected file.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        mode (str): The mode indicating whether labeling process has been started.
        file_id (int): The labeled file unique id.

    Returns:
        Renders template from which labeling the chosen file is possible.
    """

    creator_file_tracker = {"creator": username, "file_id": file_id}

    if mode == "closed":
        for item in current_app.config["LABELS"]:
            if not (item["creator"] == username and item["task_id"] == task_id and item["file_id"] == file_id):
                del item

    upload = Upload.query.filter(Upload.id == file_id).first()
    if upload.status == FILE_STATUS["CLOSED"]:
        return redirect(
            url_for(
                "user.task_files",
                username=username,
                task_id=task_id,
                file_id=file_id,
                mode="closed"
            )
        )

    for cf_tracker in current_app.config["CURRENTLY_IN_PROGRESS"]:
        if cf_tracker["file_id"] == file_id and not cf_tracker["creator"] == username:
            return redirect(
                url_for(
                    "user.task_files",
                    username=username,
                    task_id=task_id,
                    file_id=file_id,
                    mode="closed"
                )
            )

    if (creator_file_tracker not in current_app.config["CURRENTLY_IN_PROGRESS"]):
        current_app.config["CURRENTLY_IN_PROGRESS"].append(creator_file_tracker)

    upload.status = FILE_STATUS["IN PROGRESS"]
    db.session.commit()

    FILES_DIR = os.path.abspath("website/LABEL/TASKS/" + str(task_id) + "/FILES")
    directory = FILES_DIR
    if directory[len(directory) - 1] != "\\":
        directory += "\\"
    current_app.config["IMAGES"] = directory

    files = None
    for (_, _, filenames) in os.walk(current_app.config["IMAGES"]):
        files = filenames
        break
    current_app.config["FILES"] = files
    directory = current_app.config["IMAGES"]

    if file_id != 0:
        selected_filename = Upload.query.get(file_id).name
        Upload.query.get(file_id).status = FILE_STATUS["IN PROGRESS"]
        image = selected_filename
        db.session.commit()

    labels = []

    for item in current_app.config["LABELS"]:
        if item["creator"] == username and item["task_id"] == task_id and item["file_id"] == file_id:
            labels.append(item)

    predefined_labels = get_predefined_labels(
        TaskDefaultLabel.query.filter_by(task_id=task_id).all()
    )

    annotations = get_saved_labels(task_id=task_id, filename=image)

    return render_template(
        "user-label.html",
        username=username,
        task_id=task_id,
        file_id=file_id,
        directory=directory,
        image=image,
        labels=labels,
        annotations=annotations,
        labels_len=len(annotations),
        labels_all=zip(labels, annotations),
        predefined_labels=predefined_labels
    )


@labeling.route(
    "/finish-file-label/username-<string:username>/task-<int:task_id>/file-<int:file_id>"
)
@login_required
def finish_file_label(file_id, username, task_id):
    """The route for finishing file labeling process.

    Args:
        file_id (int): The file unique id.
        username (str): The username of the currently logged user who is labeling the specified file.
        task_id (int): The task unique id.

    Returns:
        Redirects to the uploaded files list within the previously selected task.
    """
    file = Upload.query.filter(Upload.id == file_id).first()
    file.status = FILE_STATUS["ANNOTATED"]
    db.session.commit()

    for cf in current_app.config["CURRENTLY_IN_PROGRESS"]:
        if cf["creator"] == username and cf["file_id"] == file_id:
            current_app.config["CURRENTLY_IN_PROGRESS"].remove(cf)
    
    return redirect(
        url_for(
            "user.task_files",
            file_id=file_id,
            task_id=task_id,
            username=username,
            mode="closed"
        )
    )


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/<string:mode>/image/<string:f>"
)
@login_required
def images(username, task_id, mode, file_id, f):
    """The route for setting displayed image.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        mode (str): The mode indicating whether labeling process has been started.
        file_id (int): The labeled file unique id.
        f (str): The file to be displayed.

    Returns:
        function: Sends the file to the client view.
    """
    images = current_app.config["IMAGES"]
    return send_file(images + f)


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/submit-labels"
)
@login_required
def submit_labels(username, task_id, file_id):
    """The route for saving labels.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        file_id (int): The labeled file unique id.

    Returns:
        Redirects to the page that allows the client to proceed with label the file.
    """
    write_annotations(task_id)

    if file_id != 0:
        selected_filename = Upload.query.get(file_id).name
        filename = selected_filename

    for label in current_app.config["LABELS"]:
        if label["creator"] == username and label["task_id"] == task_id and label["file_id"] == file_id:
            check = Annotation.query.filter_by(
                task_id=task_id,
                name=label["name"],
                creator=username,
                filename=filename,
                x_min=int(float(label["xMin"])),
                x_max=int(float(label["xMax"])),
                y_min=int(float(label["yMin"])),
                y_max=int(float(label["yMax"])),
                pose=label["pose"],
                difficult=label["difficult"],
                truncated=label["truncated"],
                occluded=label["occluded"]
            ).first()

            if check is None:
                annotation = Annotation.create(
                    nr=len(current_app.config["LABELS"]),
                    task_id=task_id,
                    name=label["name"],
                    creator=username,
                    filename=filename,
                    x_min=int(float(label["xMin"])),
                    x_max=int(float(label["xMax"])),
                    y_min=int(float(label["yMin"])),
                    y_max=int(float(label["yMax"])),
                    pose=label["pose"],
                    difficult=label["difficult"],
                    truncated=label["truncated"],
                    occluded=label["occluded"]
                )

                current_app.config["LABELS"].remove(label)

    return redirect(
        url_for(
            "labeling.task_label",
            username=username,
            task_id=task_id,
            file_id=file_id,
            mode="closed",
        )
    )


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/add/<nr>"
)
@login_required
def add_label(username, task_id, file_id, nr):
    """The route responsible for adding a new label to a session.

    Args:
        username (str):The username of the label creator.
        task_id (int): The task unique identifier.
        file_id (int): The file unique identifier.
        nr (int): The value indicating the label number within a session.

    Returns:
        Redirects to the labeling page with the newly created annotation form.
    """
    x_min = request.args.get("xMin")
    x_max = request.args.get("xMax")
    y_min = request.args.get("yMin")
    y_max = request.args.get("yMax")
    current_app.config['LABELS'].append({
        "creator": username,
        "task_id": task_id,
        "file_id": file_id,
        "image": Upload.query.filter_by(id=file_id).first().name,
        "nr": nr, 
        "name": "",
        "pose": "",
        "difficult": "",
        "truncated": "",
        "occluded": "",
        "xMin": x_min, 
        "xMax": x_max, 
        "yMin": y_min, 
        "yMax": y_max
    })

    return redirect(
        url_for(
            "labeling.task_label",
            username=username,
            task_id=task_id,
            file_id=file_id,
            mode="open"
        )
    )


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/label/<string:mode>/<int:nr>"
)
@login_required
def label_file(username, task_id, file_id, mode, nr):
    """The route for updating the label with additional information.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        mode (str): The mode indicating whether labeling process has been started.
        file_id (int): The labeled file unique id.
        nr (int): The value indicating the label number within a session.

    Returns:
        Redirects to the page for proceeding with the labeling process.
    """
    name = request.args.get("name")
    pose = request.args.get("pose")
    if not pose:
        pose = 'Unspecified'
    difficult = request.args.get("difficult")
    truncated = request.args.get("truncated")
    occluded = request.args.get("occluded")

    for label in current_app.config["LABELS"]:
        if label["creator"] == username and label["task_id"] == task_id and label["file_id"] == file_id and label["nr"] == str(nr):
            label["name"] = name
            label["pose"] = pose
            label["difficult"] = difficult
            label["truncated"] = truncated
            label["occluded"] = occluded

    return redirect(
        url_for(
            "labeling.task_label",
            username=username,
            task_id=task_id,
            file_id=file_id,
            mode="open"
        )
    )


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/remove-from-session/<int:nr>"
)
@login_required
def remove_from_session(username, task_id, file_id, nr):
    """The route for removing the annotation from the session.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        file_id (int): The labeled file unique id.
        nr (int): The value indicating the label number within a session.

    Returns:
        Redirects to the labeling main page for proceeding with creating annotations.
    """
    index = int(nr) - 1

    for item in current_app.config["LABELS"]:
        if item["creator"] == username and item["task_id"] == task_id and item["file_id"] == file_id and item["nr"] == str(nr):
            current_app.config["LABELS"].remove(item)

    for item in current_app.config["LABELS"][index:]:
        if item["creator"] == username and item["task_id"] == task_id and item["file_id"] == file_id:
            item["nr"] = str(int(item["nr"]) - 1)

    return redirect(
        url_for(
            "labeling.task_label",
            username=username,
            task_id=task_id,
            file_id=file_id,
            mode="open"
        )
    )


@labeling.route(
    "/user-<string:username>/task-<int:task_id>/file-<int:file_id>/remove-from-db/<int:id>"
)
@login_required
def remove_from_db(username, task_id, file_id, id):
    """The route for removing the annotation from the database.

    Args:
        username (str): The username of the currently logged user.
        task_id (int): The task unique identifier.
        file_id (int): The labeled file unique id.
        nr (int): The value indicating the label number within a session.

    Returns:
        Redirects to the labeling main page for proceeding with creating annotations.
    """
    check = Annotation.query.filter_by(task_id=task_id, id=id).all()
    if check is not None:
        for annotation in check:
            try:
                session_label_nr = current_app.config["LABELS"][int(annotation.nr) - 1]
                del session_label_nr
            except:
                print(
                    "[EXCEPTION] Cannot delete a label referenced by the current app configuration."
                )
            db.session.delete(annotation)
            db.session.commit()
    return redirect(
        url_for(
            "labeling.task_label",
            username=username,
            task_id=task_id,
            file_id=file_id,
            mode="open"
        )
    )


@labeling.route("/annotation-<int:annotation_id>")
@login_required
def annotation_information(annotation_id):
    """The route for displaying annotation information details.

    Args:
        annotation_id (int): The unique annotation identifier.

    Returns:
        Renders a page with details about the selected annotation.
    """
    annotation = Annotation.query.filter_by(id=annotation_id).first()
    return render_template("annotation-information.html", annotation=annotation)
