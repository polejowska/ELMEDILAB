#


### admin_access_required
```python
.admin_access_required()
```

---
The decorator used for restricting access to views dedicated only for an admin.


**Returns**

* **function**  : The decorator.


----


### add_new_user
```python
.add_new_user(
   request_approved
)
```

---
The function for adding a new user to the database.


**Args**

* **request_approved** (Request) : The request that is approved and ready to be added to the database.


----


### remove_existing_user
```python
.remove_existing_user(
   user_id
)
```

---
The function for removing the specified user from the system's databse.


**Args**

* **user_id** (int) : The user unique identifier.


----


### remove_new_request
```python
.remove_new_request(
   request_id
)
```

---
The function for removing the specified request from the system's database.


**Args**

* **request_id** (int) : The request unique identifier.


----


### configure_db_records
```python
.configure_db_records()
```

---
The function for first database setup.

