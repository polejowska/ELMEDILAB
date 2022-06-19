from website.models import FILE_STATUS, TaskUpload


def get_uploads_id(task_id):
    """The function for getting the file id.

    Args:
        task_id (int): The task unique identifier.

    Returns:
        int: The upload id.
    """
    task_uploads = TaskUpload.query.filter(TaskUpload.task_id == task_id).all()
    uploads_id = []
    for t_u in task_uploads:
        uploads_id.append(t_u.upload_id)
    return uploads_id


def change_files_status(uploads_entries, upload_annotations_num):
    """The function for file status modification.

    Args:
        uploads_entries (list): The list of uploads entries.
        upload_annotations_num (list): The list of upload annotations.
    """
    for u_e in uploads_entries:
        if upload_annotations_num[u_e.name] == 0:
            u_e.status = FILE_STATUS["NEW"]
        elif upload_annotations_num[u_e.name] > 0:
            u_e.status = FILE_STATUS["ANNOTATED"]
