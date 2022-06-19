#


### manage_tasks
```python
.manage_tasks()
```

---
The route for managing tasks.


**Returns**

Renders the template with available tasks and tools for managing or redirects to the route for creating a new task.

----


### cancel_task
```python
.cancel_task(
   id
)
```

---
The route for cancelling the specified task. The task is not submitted and not visible on the tasks list.


**Args**

* **id** (int) : The unique task identifier.


----


### create_task
```python
.create_task(
   id
)
```

---
The rout for creating a new task. When submitted, will be visible on the task list and available for users.


**Args**

* **id** (int) : The unique identifier for the newly created task.


**Returns**

Renders a template with the task's data form or redirects to the tasks list.

----


### check_task_details
```python
.check_task_details(
   task_id
)
```

---
The route for page displaying files within a selected task.


**Args**

* **task_id** (int) : The task's unique identifier.


**Returns**

Returns a template with the task's data.

----


### change_task_status
```python
.change_task_status(
   task_id, status
)
```

---
The route for modifying the task's status (possible status: "open", "closed").


**Args**

* **task_id** (int) : The task's unique identifier.
* **status** (int) : THe task's status.


**Returns**

Redirects to the page for managing tasks.

----


### change_file_status
```python
.change_file_status(
   task_id, file_id, status
)
```

---
The route for modifying file status (possible status: "new", "in progress", "annotated", "closed").


**Args**

* **task_id** (int) : The task's unique identifier.
* **file_id** (int) : The file's unique identifier.
* **status** (int) : The current status of the file within the task.


**Returns**

Redirects to the files list within a selected task.

----


### remove_task
```python
.remove_task(
   task_id
)
```

---
The route for removing the task.


**Args**

* **task_id** (id) : The task unique identifier.


**Returns**

Redirects to the managing tasks section.
