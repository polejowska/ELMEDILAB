from functools import wraps

from flask import url_for, redirect
from flask_login import current_user

from website.models import (
    ACCESS,
    Annotation,
    DefaultLabel,
    Request,
    Task,
    TaskDefaultLabel,
    TaskUpload,
    Upload,
    User,
)
from website import db


def admin_access_required():
    """The decorator used for restricting access to views dedicated only for an admin.

    Returns:
        function: The decorator.
    """
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not (
                current_user.is_authenticated and current_user.access == ACCESS["admin"]
            ):
                return redirect(url_for("auth.index"))
            return f(*args, **kwargs)
        return decorated_func
    return decorator


def add_new_user(request_approved):
    """The function for adding a new user to the database.

    Args:
        request_approved (Request): The request that is approved and ready to be added to the database.
    """
    User.create(
        username=request_approved.username,
        email=request_approved.email,
        password=request_approved.password,
        country=request_approved.country,
        education=request_approved.education,
        profession=request_approved.profession,
        additional_details=request_approved.additional_details,
    )


def remove_existing_user(user_id):
    """The function for removing the specified user from the system's databse.

    Args:
        user_id (int): The user unique identifier.
    """
    User.query.filter(User.id == user_id).delete()
    db.session.commit()


def remove_new_request(request_id):
    """The function for removing the specified request from the system's database.

    Args:
        request_id (int): The request unique identifier.
    """
    Request.query.filter(Request.id == request_id).delete()
    db.session.commit()


def configure_db_records():
    """The function for first database setup.
    """
    test_config_items = []
    test_request = Request(
        username="username_test",
        password="password_test",
        email="email@test.com",
        country="",
        profession="",
        education="",
        additional_details="",
    )
    test_config_items.append(test_request)
    test_user = User(
        username="username_user_test",
        password="password_test",
        email="email_user@test.com",
    )
    test_config_items.append(test_user)
    test_task = Task(id=1, name="test_task")
    test_config_items.append(test_task)
    test_upload = Upload(id=1, name="test_upload")
    test_config_items.append(test_upload)
    test_task_upload = TaskUpload(task_id=1, upload_id=1)
    test_config_items.append(test_task_upload)
    test_default_label = DefaultLabel(name="test_default_label")
    test_config_items.append(test_default_label)
    test_task_default_label = TaskDefaultLabel(task_id=0, default_label_id=0)
    test_config_items.append(test_task_default_label)
    test_annotation = Annotation(
        task_id=0,
        creator="test_creator",
        name="test_annotation",
        nr=0,
        filename="filename",
        x_min=0,
        x_max=0,
        y_min=0,
        y_max=0,
        pose="",
        difficult="",
        truncated="",
        occluded="",
    )
    test_config_items.append(test_annotation)

    for config_item in test_config_items:
        db.session.add(config_item)
        db.session.commit()

    admin = User(username="admin", password="administrator", email="admin@admin.com")
    admin.access = ACCESS["admin"]
    db.session.add(admin)
    db.session.commit()
