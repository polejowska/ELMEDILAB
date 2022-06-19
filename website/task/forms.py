from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms import validators
from wtforms.validators import DataRequired



CAMERA = [('1', 'A320G'), ('2', 'A655SC'), ('3', 'SC3000')]


class CreateTaskForm(FlaskForm):
    """The form specyfing a submit button that finishes the entire task creation process.
    """
    create = SubmitField("+ CREATE A NEW TASK")


class TaskForm(FlaskForm):
    """The form specifying fields that need to be filled in order to create a new task.
    """
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Enter the task name"})
    default_label = StringField("Default label", render_kw={"placeholder": "Specify the category of an object that is expected to be detected"})
    select_camera = SelectField(label="If a sequence is uploaded, please select the type of thermal camera", choices=CAMERA)
    select_frames = IntegerField('Frames frequency', [validators.NumberRange(min=1, max=1000), validators.Optional()])
    upload = SubmitField("UPLOAD")
    create = SubmitField("CREATE")
    add = SubmitField("ADD")
