"""The utils.py file for functions definitions related to a task."""

import os
import shutil

import numpy as np
import cv2

import pydicom
import png

from website.seq_processing.A655SC import generate_img_from_seq_A655SC
from website.seq_processing.SC3000 import (
    gen_images_from_seq as generate_img_from_seq_SC3000,
)
from website.seq_processing.A320G import generate_img_from_seq_A320G
from website.models import Annotation, DefaultLabel, Task, TaskDefaultLabel, TaskUpload, Upload
from website import db


EXTENSIONS_ALLOWED = {"png", "jpg", "jpeg", "bmp", "dcm", "mp4", "seq"}


def check_extension(filename):
    """The function checking whether the specific file has supported extension.

    Args:
        filename (str): The name of the file.

    Returns:
        [bool]: True if the file's extension is supported, false otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONS_ALLOWED


def add_new_files(task_id, directory):
    """The function for adding new files to the specified directory.

    Args:
        directory (str): The directory specifiying the location for adding new files.
    """
    for new_file in os.listdir(directory):
        if new_file.endswith(".png") or new_file.endswith(".jpg"):
            upload = Upload(name=new_file)
            db.session.add(upload)
            db.session.commit()
            task_upload = TaskUpload(task_id=task_id, upload_id=upload.id)
            db.session.add(task_upload)
            db.session.commit()


def add_default_label(task_id, default_label):
    """The function for adding a default label to a database and links the label to a given task.

    Args:
        task_id (int): The task's unique identifier.
        default_label (string): The category name of an object.
    """
    if DefaultLabel.query.filter_by(name=default_label).first() is None:
        default_label = DefaultLabel(name=default_label)
        db.session.add(default_label)
        db.session.commit()
    else:
        default_label = DefaultLabel.query.filter_by(name=default_label).first()
    task_default_label = TaskDefaultLabel(
        task_id=task_id, default_label_id=default_label.id
    )
    db.session.add(task_default_label)
    db.session.commit()


def get_items_names(query, table):
    """The function for getting the items names.

    Args:
        query (query): The query for searching the items.
        table (class): The table for checking the items.

    Returns:
        list: The set list of items.
    """
    names = []
    for item in query:
        if table == Upload:
            names.append(table.query.get(item.upload_id).name)
        if table == DefaultLabel:
            names.append(table.query.get(item.default_label_id).name)
    if table == DefaultLabel:
        names = set(names)
    return names


def process_save_dicom_file(file_data, directory, filename):
    """Processes and saves the uploaded DICOM file.

    Args:
        file_data (FileStorage): The DICOM file data.
        directory (str): The directory for saving the DICOM file.
        filename (str): The name of the DICOM file.
    """
    file_ds = pydicom.dcmread(file_data)
    shape = file_ds.pixel_array.shape
    img = file_ds.pixel_array.astype(float)
    img_scaled = np.uint8((np.maximum(img, 0) / img.max()) * 255.0)
    with open(os.path.join(directory, filename), "wb") as png_img:
        encoder_obj = png.Writer(file_ds.pixel_array.shape[1], shape[0], greyscale=True)
        encoder_obj.write(png_img, img_scaled)


def process_save_video_file(file_data, directory, filename, task_id):
    """Processes video file and saves frames in JPG format.

    Args:
        file_data (FileStorage): The MP4 file data.
        directory (str): The directory for saving the frames.
        filename (str): The name of the MP4 file.
        task_id (int): The unique task identifier.
    """
    file_data.save(os.path.join(directory, filename))
    video_capture = cv2.VideoCapture(directory + "//" + filename)
    success, img = video_capture.read()
    count = 0

    while success:
        path = os.path.join(directory, filename + "__frame__" + str(count) + ".jpg")
        cv2.imwrite(path, img)
        success, img = video_capture.read()
        upload = Upload(name=filename + "__frame__" + str(count) + ".jpg")
        db.session.add(upload)
        db.session.commit()
        task_upload = TaskUpload(task_id=task_id, upload_id=upload.id)
        db.session.add(task_upload)
        db.session.commit()
        count += 1


def process_save_seq_file(file_data, directory, filename, camera, frames):
    """Processes sequence file and saves frames in PNG format

    Args:
        file_data (FileStorage): The SEQ file data.
        directory (str): The directory for saving the frames.
        filename (str): The name of the SEQ file.
        camera (str): the type of camera.
        frames (int): the number specifing the frequency of saving frames.
    """
    path = os.path.join(directory, filename)
    file_data.save(path)

    if camera == "A320G":
        generate_img_from_seq_A320G(path, frames)
    if camera == "A655SC":
        generate_img_from_seq_A655SC(path, frames)
    if camera == "SC3000":
        generate_img_from_seq_SC3000(
            path, "SC3000_" + filename, directory, frames, True
        )


def make_directories(directory_files, directory_annotations):
    """The function for creating directories for annotations and files storage.

    Args:
        directory (str): The directory for files location.
        directory_annotations (str): The directory for annotations location.
    """
    os.makedirs(directory_files, exist_ok=True)
    os.makedirs(directory_annotations + "\\PASCAL_VOC_XML", exist_ok=True)
    os.makedirs(directory_annotations + "\\COCO_JSON", exist_ok=True)
    os.makedirs(directory_annotations + "\\YOLO", exist_ok=True)


def remove_directory(directory):
    """The function for removing the specified directory.

    Args:
        directory (str): The directory to be removed.
    """
    try:
        shutil.rmtree(directory)
    except OSError as exception:
        print("[ERROR]", exception.filename, exception.strerror)


def remove_db_task_data(task_id):
    """The function for removing data associated with a given task.

    Args:
        task_id (int): The unique task identifier.
    """
    query_task_upload = db.session.query(TaskUpload).filter(
        TaskUpload.task_id == task_id
    )
    for qtu in query_task_upload.all():
        db.session.query(Upload).filter(Upload.id == qtu.upload_id).delete()
    
    Annotation.query.filter_by(task_id=task_id).delete()
    query_task_upload.delete()
    db.session.query(TaskDefaultLabel).filter(
        TaskDefaultLabel.task_id == task_id
    ).delete()
    db.session.query(Task).filter(Task.id == task_id).delete()
    db.session.commit()
