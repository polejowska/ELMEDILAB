#


### check_extension
```python
.check_extension(
   filename
)
```

---
The function for checking if the file has allowed extension.


**Args**

* **filename** (str) : The name of the file.


**Returns**

* **bool**  : True if the file has allowed extension, false otherwise.


----


### write_annotations
```python
.write_annotations(
   task_id, annotation_id = None
)
```

---
The function for attaching objects to the annotation and saves to the PASCAL VOC XML file.


**Args**

* **task_id** (int) : The task unique identifier.


----


### export_annotations
```python
.export_annotations(
   task_id, filename, format
)
```

---
The function for exporting the annotations within the specified task.


**Args**

* **task_id** (int) : The task unique identifier.
* **filename** (str) : The name of the file.
* **format** (format) : The annotation format.


**Returns**

* **str**  : The download path.


----


### create_zip_archive
```python
.create_zip_archive(
   zipped_annotations_path, directory
)
```

---
The function for creating a zip archive.


**Args**

* **zipped_annotations_path** (str) : The path for saving zipped annotations.
* **directory** (str) : The directory where annotations are created.


**Returns**

* **str**  : The path to the saved zipped file.


----


### create_directory
```python
.create_directory(
   directory
)
```

---
The function for creating a new directory.

----


### clean_directory
```python
.clean_directory(
   directory
)
```

---
The function for removing the specified directory if exists.

----


### convert_prepare_uploaded_labels
```python
.convert_prepare_uploaded_labels()
```

---
The function for checking uploaded labels.

----


### convert_uploaded_labels
```python
.convert_uploaded_labels(
   input_annotation_format, output_annotation_format, task_id = None
)
```

---
The function for converting uploaded labels.

----


### get_categories
```python
.get_categories(
   xml_annotations
)
```

---
The function for getting defined categories in the PASCAL VOC XML annotations.


**Args**

* **xml_annotations** (list) : The list of annotations saved in XML files.


**Returns**

* **dict**  : The dictionary defining the category name and id.


----


### get_tree_element
```python
.get_tree_element(
   root, name, length
)
```

---
The function for getting a tree element.

----


### get_filename
```python
.get_filename(
   filename
)
```

---
The function for getting the filename without extension.

----


### convert_xml_to_json
```python
.convert_xml_to_json(
   xml_annotations, json_file, task_id
)
```

---
The function for conveerting PASCAL VOC XML annotation format to COCO JSON annotation format.


**Args**

* **xml_annotations** (list) : The list of annotations for conversion.
* **json_file** (str) : The path to JSON file.


----


### convert_json_to_yolo
```python
.convert_json_to_yolo(
   json_file, yolo_annotations
)
```

---
The function for converting COCO JSON annotation to YOLO annotation.

**Args**

* **json_file** (str) : The path to coco json file.
* **yolo_annotations** (str) : The path to yolo annotations directory.


----


### convert_xml_to_yolo
```python
.convert_xml_to_yolo(
   input_XML, json_file, output_YOLO, task_id = None
)
```

---
The function for converting PASCAL VOC XML annotation format to YOLO txt annotation format.

----


### convert_yolo_to_xml
```python
.convert_yolo_to_xml()
```

---
The function for converting YOLO TXT annotation format to PASCAL VOC XML annotation format.
