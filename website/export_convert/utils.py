from PIL import Image
from flask import request, redirect, flash

from werkzeug.utils import secure_filename
from zipfile import ZipFile
import os, shutil, glob, json
import xml.etree.ElementTree as ET

from website.models import Annotation, Task, TaskUpload, Upload
from website.pascal_voc_writer import Writer


EXTENSIONS_ALLOWED = set(["txt", "json", "xml"])
ANNOTATION_FORMAT_EXTENSION = {
    "PASCAL_VOC_XML": ".xml",
    "COCO_JSON": ".json",
    "YOLO": ".txt"
}

BBOX_START_ID = 1

PATH = os.getcwd()
INPUT_LABELS_CONVERT_FOLDER = os.path.join(PATH, "input_labels_convert")
COCO_JSON_FILE_TEMP = "website\\annotations\\COCO_JSON\\annotations.json"
YOLO_TXT_FOLDER_TEMP = "website\\annotations\\YOLO"
PASCAL_VOC_XML_FOLDER_TEMP = "website\\annotations\\PASCAL_VOC_XML"


def check_extension(filename):
    """The function for checking if the file has allowed extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file has allowed extension, false otherwise.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONS_ALLOWED


def write_annotations(task_id, annotation_id=None):
    """The function for attaching objects to the annotation and saves to the PASCAL VOC XML file.

    Args:
        task_id (int): The task unique identifier.
    """
    task_items = TaskUpload.query.filter_by(task_id=task_id).all()
    for task_item in task_items:
        upload = Upload.query.filter_by(id=task_item.upload_id).first()

        img = Image.open(
            "website\\LABEL\\TASKS\\" + str(task_id) + "\\FILES\\" + upload.name
        )

        writer = Writer(upload.name, width=img.size[0], height=img.size[1], database=Task.query.filter_by(id=task_id).first().name)

        if not annotation_id:
            annotations = Annotation.query.filter_by(
                task_id=task_id, filename=upload.name
            ).all()

            for label in annotations:
                writer.add_object(
                    name=label.name,
                    xmin=str(round(float(label.x_min))),
                    ymin=str(round(float(label.y_min))),
                    xmax=str(round(float(label.x_max))),
                    ymax=str(round(float(label.y_max))),
                    pose=label.pose,
                    difficult=label.difficult,
                    truncated=label.truncated,
                    occluded=label.occluded
                )
        else:
            label = Annotation.query.filter_by(
                task_id=task_id, id=annotation_id
            ).first()
            writer.add_object(
                name=label.name,
                xmin=str(round(float(label.x_min))),
                ymin=str(round(float(label.y_min))),
                xmax=str(round(float(label.x_max))),
                ymax=str(round(float(label.y_max))),
                pose=label.pose,
                difficult=label.difficult,
                truncated=label.truncated,
                occluded=label.occluded
            )

        writer.save(
            "website\\LABEL\\TASKS\\"
            + str(task_id)
            + "\\ANNOTATIONS\\PASCAL_VOC_XML\\"
            + upload.name
            + ".xml"
        )


def export_annotations(task_id, filename, format):
    """The function for exporting the annotations within the specified task.

    Args:
        task_id (int): The task unique identifier.
        filename (str): The name of the file.
        format (format): The annotation format.

    Returns:
        str: The download path.
    """
    path_pascal_voc_xml_annotations = (
        "website\\LABEL\\TASKS\\" + str(task_id) + "\\ANNOTATIONS\\PASCAL_VOC_XML"
    )
    coco_json_file = (
        "website\\LABEL\\TASKS\\"
        + str(task_id)
        + "\\ANNOTATIONS\\COCO_JSON\\annotations.json"
    )
    yolo_annotations = "website\\LABEL\\TASKS\\" + str(task_id) + "\\ANNOTATIONS\\YOLO"
    if filename == "None":
        path = (
            "website\\LABEL\\TASKS\\" + str(task_id) + "\\ANNOTATIONS\\" + format + "\\"
        )
        if format == "COCO_JSON":
            XML_FILES = glob.glob(
                os.path.join(
                    os.path.join(PATH, path_pascal_voc_xml_annotations), "*.xml"
                )
            )
            convert_xml_to_json(XML_FILES, coco_json_file ,task_id)
        if format == "YOLO":
            XML_FILES = glob.glob(
                os.path.join(
                    os.path.join(PATH, path_pascal_voc_xml_annotations), "*.xml"
                )
            )
            convert_xml_to_json(XML_FILES, coco_json_file, task_id)
            convert_json_to_yolo(coco_json_file, yolo_annotations)
        zipped_annotations_path = (
            "website\\LABEL\\TASKS\\"
            + str(task_id)
            + "\\ANNOTATIONS\\"
            + format
            + "_ZIPPED"
        )
        create_zip_archive(
            zipped_annotations_path=zipped_annotations_path, directory=path
        )
        zip_archive_path = (
            "LABEL\\TASKS\\" + str(task_id) + "\\ANNOTATIONS\\" + format + "_ZIPPED.zip"
        )
        return zip_archive_path
    else:
        if format == "PASCAL_VOC_XML":
            return (
                "LABEL\\TASKS\\"
                + str(task_id)
                + "\\ANNOTATIONS\\"
                + format
                + "\\"
                + filename
                + ANNOTATION_FORMAT_EXTENSION[format]
            )
        if format == "YOLO":
            return (
                "LABEL\\TASKS\\"
                + str(task_id)
                + "\\ANNOTATIONS\\"
                + format
                + "\\"
                + os.path.splitext(filename)[0]
                + ANNOTATION_FORMAT_EXTENSION[format]
            )


def create_zip_archive(zipped_annotations_path, directory):
    """The function for creating a zip archive.

    Args:
        zipped_annotations_path (str): The path for saving zipped annotations.
        directory (str): The directory where annotations are created.

    Returns:
        str: The path to the saved zipped file.
    """
    with ZipFile(zipped_annotations_path + ".zip", "w") as zip_obj:
        for folder, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(folder, filename)
                zip_obj.write(file_path, os.path.basename(file_path))
    zip_obj.close()
    return zipped_annotations_path + ".zip"


def create_directory(directory):
    """The function for creating a new directory."""
    if not os.path.isdir(directory):
        os.mkdir(directory)
    else:
        clean_directory(directory)


def clean_directory(directory):
    """The function for removing the specified directory if exists."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("[EXCEPTION] Failed to delete %s. Reason: %s' % (file_path, e)")


def convert_prepare_uploaded_labels():
    """The function for checking uploaded labels."""
    create_directory(INPUT_LABELS_CONVERT_FOLDER)
    if request.method == "POST":
        if "files[]" not in request.files:
            flash("No file part")
            return redirect(request.url)
        files = request.files.getlist("files[]")
        for file in files:
            if file and check_extension(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(INPUT_LABELS_CONVERT_FOLDER, filename))


def convert_uploaded_labels(input_annotation_format, output_annotation_format, task_id=None):
    """The function for converting uploaded labels."""

    XML_TEMP_FILES = glob.glob(
        os.path.join(os.path.join(PATH, "input_labels_convert"), "*.xml")
    )

    if (
        input_annotation_format == "YOLO"
        and output_annotation_format == "PASCAL VOC XML"
    ):
        convert_yolo_to_xml()
    if (
        input_annotation_format == "PASCAL VOC XML"
        and output_annotation_format == "COCO JSON"
    ):
        convert_xml_to_json(XML_TEMP_FILES, COCO_JSON_FILE_TEMP, task_id)
    if input_annotation_format == "COCO JSON" and output_annotation_format == "YOLO":
        convert_json_to_yolo(
            json_file=COCO_JSON_FILE_TEMP, yolo_annotations=YOLO_TXT_FOLDER_TEMP
        )
    if (
        input_annotation_format == "PASCAL VOC XML"
        and output_annotation_format == "YOLO"
    ):
        convert_xml_to_yolo(
            input_XML=XML_TEMP_FILES,
            json_file=COCO_JSON_FILE_TEMP,
            output_YOLO=YOLO_TXT_FOLDER_TEMP,
        )


def get_categories(xml_annotations):
    """The function for getting defined categories in the PASCAL VOC XML annotations.

    Args:
        xml_annotations (list): The list of annotations saved in XML files.

    Returns:
        dict: The dictionary defining the category name and id.
    """
    categories = []
    for xml_annotation in xml_annotations:
        tree = ET.parse(xml_annotation)
        root = tree.getroot()
        for object in root.findall("object"):
            categories.append(object[0].text)
    categories = list(set(categories))
    return {
        category: c for c, category in enumerate(categories) if category is not None
    }


def get(root, name):
    """The function for getting nodes according to the specified name and root."""
    vars = root.findall(name)
    return vars


def get_tree_element(root, name, length):
    """The function for getting a tree element."""
    vars = root.findall(name)
    if length == 1:
        vars = vars[0]
    return vars


def get_filename(filename):
    """The function for getting the filename without extension."""
    filename = filename.replace("\\", "/")
    filename = os.path.splitext(os.path.basename(filename))[0]
    return str(filename)


def convert_xml_to_json(xml_annotations, json_file, task_id):
    """The function for conveerting PASCAL VOC XML annotation format to COCO JSON annotation format.

    Args:
        xml_annotations (list): The list of annotations for conversion.
        json_file (str): The path to JSON file.
    """
    json_dictionary = {
        "images": [],
        "type": "instances",
        "annotations": [],
        "categories": [],
    }
    categories = get_categories(xml_annotations)
    
    for xml_annotation in xml_annotations:
        tree = ET.parse(xml_annotation)
        root = tree.getroot()
        path = get(root, "path")
        if len(path) == 1:
            filename = os.path.basename(path[0].text)
        elif len(path) == 0:
            filename = get_tree_element(root, "filename", 1).text

        image_id = Upload.query.filter_by(name=filename).first().id

        uploads = TaskUpload.query.filter_by(task_id=task_id).all()

        if task_id is not None:
            for upload in uploads:
                upload_query = Upload.query.filter_by(id=upload.id).first()
                if upload_query.name == filename:
                    image_id = upload_query.id

        size = get_tree_element(root, "size", 1)
        width = int(get_tree_element(size, "width", 1).text)
        height = int(get_tree_element(size, "height", 1).text)
        image = {
            "file_name": filename,
            "height": height,
            "width": width,
            "id": image_id,
        }
        json_dictionary["images"].append(image)

        bbox_id = BBOX_START_ID

        for object in get(root, "object"):
            category = get_tree_element(object, "name", 1).text
            if category not in categories:
                new_id = len(categories)
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_tree_element(object, "bndbox", 1)
            xmin = float(get_tree_element(bndbox, "xmin", 1).text)
            ymin = float(get_tree_element(bndbox, "ymin", 1).text)
            xmax = float(get_tree_element(bndbox, "xmax", 1).text)
            ymax = float(get_tree_element(bndbox, "ymax", 1).text)
            o_width = int(abs(xmax - xmin))
            o_height = int(abs(ymax - ymin))
            annotation = {
                "area": o_width * o_height,
                "iscrowd": 0,
                "image_id": image_id,
                "bbox": [int(xmin), int(ymin), o_width, o_height],
                "category_id": category_id,
                "id": bbox_id,
                "ignore": 0,
                "segmentation": [],
            }
            json_dictionary["annotations"].append(annotation)
            bbox_id = bbox_id + 1

    for name, id in categories.items():
        category = {"supercategory": "none", "id": id, "name": name}
        json_dictionary["categories"].append(category)

    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    json_fp = open(json_file, "w")
    json_str = json.dumps(json_dictionary)
    json_fp.write(json_str)
    json_fp.close()


def convert_bbox_coco_to_yolo(bbox, img_width, img_height):
    """The function for converting bounding box from COCO format to YOLO format.
    YOLO bounding box format: [x_center, y_center, width, height]

    Args:
        img_width (int): The width of the image.
        img_height (int): The height of the image.
        bbox (list, int): The bounding box in COCO format: [x_max, y_max, width, height].

    Returns:
        list (float): The bounding box annotation in YOLO format.
    """
    x_top_left, y_top_left, w, h = bbox

    x_center = x_top_left + w / 2.0
    y_center = y_top_left + h / 2.0

    x = round(x_center * (1.0 / img_width), 6)
    y = round(y_center * (1.0 / img_height), 6)
    w = round(w * (1.0 / img_width), 6)
    h = round(h * (1.0 / img_height), 6)

    return [x, y, w, h]


def convert_json_to_yolo(json_file, yolo_annotations):
    """The function for converting COCO JSON annotation to YOLO annotation.
    Args:
        json_file (str): The path to coco json file.
        yolo_annotations (str): The path to yolo annotations directory.
    """
    create_directory(yolo_annotations)

    with open(json_file, "r") as f:
        annotation = json.load(f)
    for img in annotation["images"]:
        image_id = img["id"]
        file_name = img["file_name"]
        img_width = img["width"]
        img_height = img["height"]
        values = filter(
            lambda item: item["image_id"] == image_id, annotation["annotations"]
        )
        output_yolo_file = open(yolo_annotations + "\\" + file_name[:-4] + ".txt", "a+")
        for value in values:
            bbox = value["bbox"]
            x, y, w, h = convert_bbox_coco_to_yolo(bbox, img_width, img_height)
            bndbox = (x, y, w, h)
            output_yolo_file.write(
                str(value["category_id"])
                + " "
                + " ".join([str(c) for c in bndbox])
                + "\n"
            )
        output_yolo_file.close()

    create_zip_archive(yolo_annotations, yolo_annotations)


def convert_xml_to_yolo(input_XML, json_file, output_YOLO, task_id=None):
    """The function for converting PASCAL VOC XML annotation format to YOLO txt annotation format."""
    convert_xml_to_json(input_XML, json_file=json_file, task_id=None)
    convert_json_to_yolo(json_file=json_file,yolo_annotations=output_YOLO)


def convert_yolo_to_xml():
    """The function for converting YOLO TXT annotation format to PASCAL VOC XML annotation format."""
    create_directory(PASCAL_VOC_XML_FOLDER_TEMP)
