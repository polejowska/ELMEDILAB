#


### task_submitted_labels
```python
.task_submitted_labels(
   task_id
)
```

---
The route for displaying and saving annotations.


**Args**

* **task_id** (int) : The unique task identifier.


**Returns**

Renders template with submitted labels in the selected task.

----


### export_json_file
```python
.export_json_file()
```

---
The route for downloading COCO JSON annotation.


**Returns**

* **function**  : Saves the json file with annotations created.


----


### export_label
```python
.export_label(
   task_id, annotation_id
)
```

---
The route for downloading the selected annotation.


**Args**

* **task_id** (int) : The task unique identifier.
* **annotation_id** (int) : The annotation unique identifier.


**Returns**

* **function**  : Saves the file locally.


----


### export_labels
```python
.export_labels()
```

---
The route for exporting labels according to the displayed form.


**Returns**

Renders template with the form responsible for exporting labels.

----


### export
```python
.export(
   task_id, format, filename
)
```

---
The route for exporting labels from the submitted labels list.


**Args**

* **task_id** (int) : The task unique identifier.
* **format** (str) : The label format.
* **filename** (str) : The name of the file annotated.


**Returns**

* **function**  : Downloads labels according to the selected format, the task id and the filename.


----


### remove_label
```python
.remove_label(
   task_id, annotation_id
)
```

---
The route for removing the selected label.


**Args**

* **task_id** (int) : The task unique identifier.
* **annotation_id** (int) : The annotation unique identifier.


**Returns**

Redirects to the submitted labels page.

----


### task_submitted_labels
```python
.task_submitted_labels(
   task_id
)
```

---
The route for displaying and saving annotations.


**Args**

* **task_id** (int) : The unique task identifier.


**Returns**

Renders template with submitted labels in the selected task.

----


### task_filename_submitted_labels
```python
.task_filename_submitted_labels(
   task_id, filename
)
```

---
The route for accessing filtered submitted labels list based on the annotation creator.


**Args**

* **task_id** (int) : The task unique identifier.
* **filename** (str) : The name of the file.


**Returns**

Renders template with submitted labels in the selected task and filtered by filename.

----


### task_creator_submitted_labels
```python
.task_creator_submitted_labels(
   task_id, creator
)
```

---
The route for accessing filtered submitted labels list based on the annotation creator.


**Args**

* **task_id** (int) : The task unique identifier.
* **creator** (str) : The username of the annotation creator.


**Returns**

Renders template with submitted labels in the selected task and filtered by the creator.

----


### convert_labels
```python
.convert_labels()
```

---
The route dedicated for annotations formats conversion.


**Returns**

* **funtion**  : Saves the converted annotation.
Renders the template with the label format conversion form.
