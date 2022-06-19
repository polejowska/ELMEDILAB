"""Models specification."""

from datetime import datetime

from flask_login import UserMixin

from website import db, login_manager, bcrypt


ACCESS = {"user": 1, "admin": 2}
TASK_STATUS = {"INACTIVE": 0, "ACTIVE": 1}
FILE_STATUS = {"NEW": 0, "IN PROGRESS": 1, "ANNOTATED": 2, "CLOSED": 3}


@login_manager.user_loader
def load_user(user_id):
    """Handles logging in and logging out by storing user's ID.

    Args:
        user_id (int): The number indentifing the user.

    Returns:
        User: The user object indicated by user ID number.
    """
    return User.query.get(int(user_id))


class BaseMixin(object):
    """The base class for saving objects to a database.

    Args:
        object (class): The object to be added and commited to a database.
    """

    @classmethod
    def create(cls, **kw):
        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()


class Request(db.Model, BaseMixin):
    """The database model for request table.

    Args:
        db (db.Model): The default db model.
        BaseMixin (BaseMixin): The BaseMixin for saving objects to the database.
    """

    __tablename__ = "request"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    date_requested = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(120), nullable=True)
    profession = db.Column(db.String(120), nullable=True)
    education = db.Column(db.String(120), nullable=True)
    additional_details = db.Column(db.Text, nullable=True)

    def __init__(
        self,
        username,
        email,
        password,
        country="",
        profession="",
        education="",
        additional_details="",
    ):
        """Initializes the request.

        Args:
            username (str): The username.
            email (str): The user's email.
            password (str): The user's password.
            country (str, optional): The user's country. Defaults to "".
            profession (str, optional): The user's profession. Defaults to "".
            education (str, optional): The user's education. Defaults to "".
            additional_details (str, optional): Additional details about the user. Defaults to "".
        """
        self.username = username
        self.email = email
        self.password = self.generate_pwd_hash(password)
        self.country = country
        self.profession = profession
        self.education = education
        self.additional_details = additional_details

    @staticmethod
    def generate_pwd_hash(password):
        """Generates password hash using bcrypt module.

        Args:
            password (string): The user's password.

        Returns:
            password: The hashed password.
        """
        return bcrypt.generate_password_hash(password).decode("utf-8")


class User(db.Model, BaseMixin, UserMixin):
    """The database model for user table.

    Args:
        db (db.Model): The default db model.
        BaseMixin (BaseMixin): The BaseMixin for saving objects to the database.
        UserMixin (UserMixin): The UserMixin for accessing special methods.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    country = db.Column(db.String(120), nullable=True)
    profession = db.Column(db.String(120), nullable=True)
    education = db.Column(db.String(120), nullable=True)
    additional_details = db.Column(db.Text, nullable=True)
    access = db.Column(db.Integer, default=ACCESS["user"])

    def __init__(
        self,
        username,
        email,
        password,
        country="",
        profession="",
        education="",
        additional_details="",
    ):
        """Initializes the user.

        Args:
            username (str): The username.
            email (str): The user's email.
            password (str): The user's password.
            country (str, optional): The user's country. Defaults to "".
            profession (str, optional): The user's profession. Defaults to "".
            education (str, optional): The user's education. Defaults to "".
            additional_details (str, optional): Additional details about the user. Defaults to "".
        """
        self.username = username
        self.email = email
        self.password = password
        self.country = country
        self.profession = profession
        self.education = education
        self.additional_details = additional_details


class Task(db.Model, BaseMixin):
    """The database model for task table.

    Args:
        db (db.Model): The default db model.
        BaseMixin (BaseMixin): The BaseMixin for saving objects to the database.
    """

    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=TASK_STATUS["INACTIVE"])

    def __init__(self, id, name):
        """Initializes the task.

        Args:
            id (int): The unique idenitifier for the task.
            name (str): The name of the task.
        """
        self.id = id
        self.name = name


class Upload(db.Model):
    """The database model for upload table.

    Args:
        db (db.Model): The default db model.
    """

    __tablename__ = "upload"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text, nullable=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer, default=FILE_STATUS["NEW"])


class TaskUpload(db.Model):
    """The database model for association table between task and upload table.

    Args:
        db (db.Model): The default db model.
    """

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    upload_id = db.Column(db.Integer, nullable=False)


class DefaultLabel(db.Model):
    """The database model for default label table.

    Args:
        db (db.Model): The default db model.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)

    def __init__(self, name):
        """Initializes default label category.

        Args:
            name (str): The category object name.
        """
        self.name = name


class TaskDefaultLabel(db.Model):
    """The database model for the association table between task and default label table.

    Args:
        db (db.Model): The default db model.
    """

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    default_label_id = db.Column(db.Integer, nullable=False)


class Annotation(db.Model, BaseMixin):
    """The database model for annotation table.

    Args:
        db (db.Model): The default db model.
        BaseMixin (BaseMixin): The class for saving objects to the database.
    """

    __tablename__ = "annotation"
    id = db.Column(db.Integer, primary_key=True)
    nr = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    creator = db.Column(db.String(20), nullable=False)
    name = db.Column(db.Text, nullable=True)
    pose = db.Column(db.Text, nullable=True)
    truncated = db.Column(db.Text, nullable=True)
    difficult = db.Column(db.Text, nullable=True)
    occluded = db.Column(db.Text, nullable=True)
    x_max = db.Column(db.Integer, nullable=True)
    y_max = db.Column(db.Integer, nullable=True)
    x_min = db.Column(db.Integer, nullable=True)
    y_min = db.Column(db.Integer, nullable=True)
    filename = db.Column(db.Text, nullable=True)
    path = db.Column(db.Text, nullable=True)
    database = db.Column(db.Text, nullable=True)
    width = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    depth = db.Column(db.Integer, nullable=True)
    
    def __init__(
        self,
        nr,
        task_id,
        creator,
        name,
        pose,
        truncated,
        difficult,
        occluded,
        x_max,
        y_max,
        x_min,
        y_min,
        filename,
    ):
        """Initializes the annotation.

        Args:
            nr (int): The annotation number.
            task_id (int): The task identifier in which annotation is generated.
            creator (str): The username of the annotation creator.
            name (str): The category name of the object annotated.
            pose (str): The pose of the object annotated.
            truncated (str): The value indicating whether the annotated object is truncated.
            difficult (str): The value indicating whether the annotated object is difficult.
            occluded (str): The value indicating whether the annotated object is occluded.
            x_max (str): The highest x coordinate of the bounding box.
            y_max (str): The highest y coordinate of the bounding box.
            x_min (str): The lowest x coordinate of the bounding box.
            y_min (str): The lowest y coordinate of the bounding box.
            filename (str): The filename of the image being annotated.
        """
        self.nr = nr
        self.task_id = task_id
        self.name = name
        self.creator = creator
        self.pose = pose
        self.truncated = truncated
        self.difficult = difficult
        self.occluded = occluded
        self.x_max = x_max
        self.y_max = y_max
        self.x_min = x_min
        self.y_min = y_min
        self.filename = filename
