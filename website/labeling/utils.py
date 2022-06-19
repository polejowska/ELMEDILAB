from website.models import Annotation, DefaultLabel
from website import db


def save_label(label):
    """The function for saving the created label to the database.

    Args:
        label (Annotation): The annotation object to be saved.
    """
    db.session.add(label)
    db.session.commit()


def remove_label(label):
    """The function for removing the created label from the database.

    Args:
        label (Annotation): The annotation object to be removed.
    """
    db.session.delete(label)
    db.session.commit()


def get_saved_labels(task_id, filename):
    """The function for getting the saved labels according to the task id and filename.

    Args:
        task_id (int): The task unique identifier.
        filename (str): The name of the file.

    Returns:
        list: The list of saved labels correlated to the specified filename and task id.
    """
    saved_labels = Annotation.query.filter_by(task_id=task_id, filename=filename).all()
    return saved_labels


def get_predefined_labels(query):
    """The function for getting categories related to the specific task.

    Args:
        query (list): The list of items within a query.

    Returns:
        list: The list of predefined labels for the given task specified in the query.
    """
    predefined_labels = []
    for item in query:
        predefined_labels.append(
            DefaultLabel.query.filter_by(id=item.default_label_id).first().name
        )
    return predefined_labels
