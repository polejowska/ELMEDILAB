from flask import (
    render_template,
    redirect,
    url_for,
    send_file,
    Blueprint,
    request,
    flash,
)
from website.admin.utils import admin_access_required

from website.export_convert.utils import (
    ANNOTATION_FORMAT_EXTENSION,
    convert_prepare_uploaded_labels,
    convert_uploaded_labels,
    export_annotations,
    write_annotations,
)
from website.export_convert.forms import ANNOTATION_FORMATS, ExportForm, ConvertForm, ExportSubmitted
from website.models import Annotation, Task
from website import db


export_convert = Blueprint("export_convert", __name__)


@export_convert.route("/admin/tasks/submitted-labels", methods=["GET", "POST"])
@admin_access_required()
def tasks_submitted_labels():
    """The route for displaying available tasks.

    Returns:
        Renders template with task with submitted labels.
    """
    tasks = Task.query.order_by(Task.id)
    return render_template("admin-tasks-submitted-labels.html", tasks=tasks)


@export_convert.route("/admin/tasks/submitted-labels/json/export")
@admin_access_required()
def export_json_file():
    """The route for downloading COCO JSON annotation.

    Returns:
        function: Saves the json file with annotations created.
    """
    path = "annotations\\COCO_JSON\\annotations.json"
    return send_file(path, as_attachment=True)


@export_convert.route(
    "/admin/remove-label/task-<int:task_id>/annotation-<int:annotation_id>"
)
@admin_access_required()
def remove_label(task_id, annotation_id):
    """The route for removing the selected label.

    Args:
        task_id (int): The task unique identifier.
        annotation_id (int): The annotation unique identifier.

    Returns:
        Redirects to the submitted labels page.
    """
    db.session.query(Annotation).filter(Annotation.id == annotation_id).delete()
    db.session.commit()
    write_annotations(task_id)
    return redirect(url_for("export_convert.task_submitted_labels", task_id=task_id))


@export_convert.route(
    "/admin/export-label/task-<int:task_id>/annotation-<int:annotation_id>"
)
@admin_access_required()
def export_label(task_id, annotation_id):
    """The route for downloading the selected annotation.

    Args:
        task_id (int): The task unique identifier.
        annotation_id (int): The annotation unique identifier.

    Returns:
        function: Saves the file locally.
    """
    write_annotations(task_id, annotation_id)
    filename = (
        Annotation.query.filter(
            Annotation.task_id == task_id, Annotation.id == annotation_id
        )
        .first()
        .filename
    )
    download_path = (
        "LABEL\\TASKS\\"
        + str(task_id)
        + "\\ANNOTATIONS\\PASCAL_VOC_XML\\"
        + filename
        + ANNOTATION_FORMAT_EXTENSION["PASCAL_VOC_XML"]
    )
    return send_file(download_path, as_attachment=True)


@export_convert.route(
    "/admin/task-<int:task_id>/submitted-labels", methods=["GET", "POST"]
)
@admin_access_required()
def task_submitted_labels(task_id):
    """The route for displaying and saving annotations.

    Args:
        task_id (int): The unique task identifier.

    Returns:
        Renders template with submitted labels in the selected task.
    """
    form = ExportSubmitted()

    if form.validate_on_submit():
        if form.export_pascal_voc.data:
            return redirect(
                url_for(
                    "export_convert.export",
                    format='PASCAL VOC XML',
                    task_id=task_id,
                    filename="None",
                )
            )
        if form.export_coco.data:
            return redirect(
                url_for(
                    "export_convert.export",
                    format='COCO JSON',
                    task_id=task_id,
                    filename="None",
                )
            )
        if form.export_yolo.data:
            return redirect(
                url_for(
                    "export_convert.export",
                    format='YOLO',
                    task_id=task_id,
                    filename="None",
                )
            )


    annotations = Annotation.query.filter_by(task_id=task_id)
    return render_template(
        "admin-task-submitted-labels.html",
        task_id=task_id,
        form=form,
        filename=None,
        annotations=annotations,
        labels_len=len(annotations.all()),
    )


@export_convert.route(
    "/admin/task-<int:task_id>/submitted-labels/filename-<string:filename>",
    methods=["GET", "POST"],
)
@admin_access_required()
def task_filename_submitted_labels(task_id, filename):
    """The route for accessing filtered submitted labels list based on the annotation creator.

    Args:
        task_id (int): The task unique identifier.
        filename (str): The name of the file.

    Returns:
        Renders template with submitted labels in the selected task and filtered by filename.
    """
    annotations = Annotation.query.filter_by(task_id=task_id, filename=filename)
    return render_template(
        "admin-task-filter-submitted-labels.html",
        task_id=task_id,
        filename=filename,
        annotations=annotations,
        labels_len=len(annotations.all()),
    )


@export_convert.route(
    "/admin/task-<int:task_id>/submitted-labels/creator-<string:creator>",
    methods=["GET", "POST"],
)
@admin_access_required()
def task_creator_submitted_labels(task_id, creator):
    """The route for accessing filtered submitted labels list based on the annotation creator.

    Args:
        task_id (int): The task unique identifier.
        creator (str): The username of the annotation creator.

    Returns:
        Renders template with submitted labels in the selected task and filtered by the creator.
    """
    annotations = Annotation.query.filter_by(task_id=task_id, creator=creator)
    return render_template(
        "admin-task-filter-submitted-labels.html",
        task_id=task_id,
        annotations=annotations,
    )


@export_convert.route("/admin/export-labels", methods=["GET", "POST"])
@admin_access_required()
def export_labels():
    """The route for exporting labels according to the displayed form.

    Returns:
        Renders template with the form responsible for exporting labels.
    """
    export_form = ExportForm()
    tasks = Task.query.all()
    tasks_ids = []
    for task in tasks:
        if task.id not in tasks_ids:
            tasks_ids.append(int(task.id))
    if export_form.validate_on_submit():
        output_annotation_format = dict(ANNOTATION_FORMATS).get(
            export_form.output_format.data
        )
        task_id = int(request.form["task_id"])
        if task_id in tasks_ids:
            return redirect(
                url_for(
                    "export_convert.export",
                    format=output_annotation_format,
                    task_id=task_id,
                    filename="None",
                )
            )
        flash("Invalid task id provided", "warning")
    return render_template("admin-export-labels.html", form=export_form, tasks=tasks)


@export_convert.route(
    "/admin/export/<int:task_id>/<string:format>/<string:filename>",
    methods=["GET", "POST"],
)
@admin_access_required()
def export(task_id, format, filename):
    """The route for exporting labels from the submitted labels list.

    Args:
        task_id (int): The task unique identifier.
        format (str): The label format.
        filename (str): The name of the file annotated.

    Returns:
        function: Downloads labels according to the selected format, the task id and the filename.
    """
    if format == "PASCAL VOC XML": format = "PASCAL_VOC_XML"
    if format == "COCO JSON": format = "COCO_JSON"

    write_annotations(task_id)

    download_path = export_annotations(
        task_id=task_id, filename=filename, format=format
    )

    if filename == "None":
        return send_file(download_path, mimetype="application/zip", as_attachment=True)
    else:
        return send_file(download_path, as_attachment=True)


@export_convert.route("/admin/convert-labels", methods=["POST", "GET"])
@admin_access_required()
def convert_labels():
    """The route dedicated for annotations formats conversion.

    Returns:
        funtion: Saves the converted annotation.
        Renders the template with the label format conversion form.
    """
    convert_form = ConvertForm()
    if convert_form.validate_on_submit():
        input_annotation_format = dict(ANNOTATION_FORMATS).get(
            convert_form.input_format.data
        )
        output_annotation_format = dict(ANNOTATION_FORMATS).get(
            convert_form.output_format.data
        )
        convert_prepare_uploaded_labels()
        if (
            input_annotation_format == "PASCAL VOC XML"
            and output_annotation_format == "COCO JSON"
        ):
            convert_uploaded_labels(input_annotation_format, output_annotation_format)
            return redirect(url_for("export_convert.export_json_file"))
        if (
            input_annotation_format == "PASCAL VOC XML"
            or input_annotation_format == "COCO JSON"
        ) and output_annotation_format == "YOLO":
            convert_uploaded_labels(input_annotation_format, output_annotation_format)
            return send_file(
                "annotations\\YOLO.zip", mimetype="application/zip", as_attachment=True
            )
        if (
            input_annotation_format == "YOLO"
            and output_annotation_format == "PASCAL VOC XML"
        ):
            convert_uploaded_labels(input_annotation_format, output_annotation_format)
            return send_file(
                "annotations\\PASCAL_VOC_XML.zip",
                mimetype="application/zip",
                as_attachment=True
            )
    return render_template("admin-convert-labels.html", form=convert_form)
