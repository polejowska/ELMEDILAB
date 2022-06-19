#


### admin_main
```python
.admin_main()
```

---
The route to admin main panel.


**Returns**

Renders admin-main.html template.

----


### approve_requests
```python
.approve_requests()
```

---
The route for approving requests.


**Returns**

Renders template with requests management panel.

----


### add_user
```python
.add_user(
   request_id
)
```

---
The route for adding new user.


**Args**

* **request_id** (int) : The request unique identifier.


**Returns**

Redirects to requests list.

----


### users
```python
.users()
```

---
The route for managing users.


**Returns**

Renders a page with users list.

----


### remove_request
```python
.remove_request(
   request_id
)
```

---
The route for removing the request.


**Args**

* **request_id** (int) : The request's unique identifier.


**Returns**

Redirects to modified requests list.

----


### remove_user
```python
.remove_user(
   user_id
)
```

---
The route for removing the user.


**Args**

* **user_id** (int) : The user's unique identifier.


**Returns**

Redirects to modified users list.
