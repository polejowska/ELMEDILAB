#


### save_label
```python
.save_label(
   label
)
```

---
The function for saving the created label to the database.


**Args**

* **label** (Annotation) : The annotation object to be saved.


----


### remove_label
```python
.remove_label(
   label
)
```

---
The function for removing the created label from the database.


**Args**

* **label** (Annotation) : The annotation object to be removed.


----


### get_saved_labels
```python
.get_saved_labels(
   task_id, filename
)
```

---
The function for getting the saved labels according to the task id and filename.


**Args**

* **task_id** (int) : The task unique identifier.
* **filename** (str) : The name of the file.


**Returns**

* **list**  : The list of saved labels correlated to the specified filename and task id.

