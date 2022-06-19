#


### task_label
```python
.task_label(
   username, task_id, mode, file_id
)
```

---
The route for managing mechanisms related to starting labeling the selected file.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **mode** (str) : The mode indicating whether labeling process has been started.
* **file_id** (int) : The labeled file unique id.


**Returns**

Renders template from which labeling the chosen file is possible.

----


### finish_file_label
```python
.finish_file_label(
   file_id, username, task_id
)
```

---
The route for finishing file labeling process.


**Args**

* **file_id** (int) : The file unique id.
* **username** (str) : The username of the currently logged user who is labeling the specified file.
* **task_id** (int) : The task unique id.


**Returns**

Redirects to the uploaded files list within the previously selected task.

----


### images
```python
.images(
   username, task_id, mode, file_id, f
)
```

---
The route for setting displayed image.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **mode** (str) : The mode indicating whether labeling process has been started.
* **file_id** (int) : The labeled file unique id.
* **f** (str) : The file to be displayed.


**Returns**

* **function**  : Sends the file to the client view.


----


### submit_labels
```python
.submit_labels(
   username, task_id, file_id
)
```

---
The route for saving labels.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **file_id** (int) : The labeled file unique id.


**Returns**

Redirects to the page that allows the client to proceed with label the file.

----


### add_label
```python
.add_label(
   username, task_id, file_id, nr
)
```

---
The route responsible for adding a new label to a session.


**Args**

* **task_id** (int) : The task unique identifier.
* **file_id** (int) : The file unique identifier.
* **nr** (int) : The value indicating the label number within a session.
username (str):The username of the label creator.


**Returns**

Redirects to the labeling page with the newly created annotation form.

----


### label_file
```python
.label_file(
   username, task_id, file_id, mode, nr
)
```

---
The route for updating the label with additional information.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **mode** (str) : The mode indicating whether labeling process has been started.
* **file_id** (int) : The labeled file unique id.
* **nr** (int) : The value indicating the label number within a session.


**Returns**

Redirects to the page for proceeding with the labeling process.

----


### remove_from_session
```python
.remove_from_session(
   username, task_id, file_id, nr
)
```

---
The route for removing the annotation from the session.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **file_id** (int) : The labeled file unique id.
* **nr** (int) : The value indicating the label number within a session.


**Returns**

Redirects to the labeling main page for proceeding with creating annotations.

----


### remove_from_db
```python
.remove_from_db(
   username, task_id, file_id, id
)
```

---
The route for removing the annotation from the database.


**Args**

* **username** (str) : The username of the currently logged user.
* **task_id** (int) : The task unique identifier.
* **file_id** (int) : The labeled file unique id.
* **nr** (int) : The value indicating the label number within a session.


**Returns**

Redirects to the labeling main page for proceeding with creating annotations.

----


### annotation_information
```python
.annotation_information(
   annotation_id
)
```

---
The route for displaying annotation information details.


**Args**

* **annotation_id** (int) : The unique annotation identifier.


**Returns**

Renders a page with details about the selected annotation.
