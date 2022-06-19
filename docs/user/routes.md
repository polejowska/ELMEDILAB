#


### user_main
```python
.user_main(
   username
)
```

---
The route for main user panel.


**Args**

* **username** (str) : The username.


**Returns**

Renders a page with user panel displaying available options.

----


### profile
```python
.profile(
   username
)
```

---
The route for user profile form.


**Args**

* **username** (str) : The username.


**Returns**

Renders a page with user profile.

----


### tasks
```python
.tasks(
   username
)
```

---
The route for the list of tasks.


**Args**

* **username** (str) : The username.


**Returns**

Renders the template with tasks.

----


### task_files
```python
.task_files(
   username, task_id
)
```

---
"The route dedicated for files included in a task operations.


**Args**

* **username** (str) : The username.
* **task_id** (int) : The task unique identifier.


**Returns**

Renders a page with files included in a chosen task.

----


### display_user_profile
```python
.display_user_profile(
   username
)
```

---
The route for the other than the current user user profile page.


**Args**

* **username** (str) : The username of the user which profile is selected.


**Returns**

Renders the page with the user profile.
