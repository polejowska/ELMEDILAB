from flask_wtf.form import FlaskForm
from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import ValidationError

from website.models import Task


ANNOTATION_FORMATS = [("1", "PASCAL VOC XML"), ("2", "COCO JSON"), ("3", "YOLO")]


class ExportForm(FlaskForm):
    """The form for exporting annotations.

    Raises:
        ValidationError: Raised when specified task id does not exist.
    """

    output_format = SelectField(
        label="OUTPUT ANNOTATIONS FORMAT", choices=ANNOTATION_FORMATS
    )
    export = SubmitField("EXPORT")

    def validate_task_id(self, task_id):
        """Checks task id validity.

        Args:
            task_id (int): The unique task identifier.
        """
        tasks = Task.query.filter_by(id=task_id).all()
        tasks_ids = []
        for task in tasks:
            tasks_ids.append(task.id)
        if task_id not in tasks_ids:
            raise ValidationError("This task ID does not exist.")


class ExportSubmitted(FlaskForm):
    """The form for exporting submitted labels.
    """
    export_pascal_voc = SubmitField("PASCAL VOC XML")
    export_coco = SubmitField("COCO JSON")
    export_yolo = SubmitField("YOLO")


class ConvertForm(FlaskForm):
    """The form for annotations format conversion.
    """
    input_format = SelectField(
        label="INPUT ANNOTATIONS FORMAT", choices=ANNOTATION_FORMATS
    )
    output_format = SelectField(
        label="OUTPUT ANNOTATIONS FORMAT", choices=ANNOTATION_FORMATS
    )
    convert = SubmitField("CONVERT AND DOWNLOAD")
