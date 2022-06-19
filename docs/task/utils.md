#


### check_extension
```python
.check_extension(
   filename
)
```

---
The function checking whether the specific file has supported extension.


**Args**

* **filename** (str) : The name of the file.


**Returns**

* True if the file's extension is supported, false otherwise.


----


### add_new_files
```python
.add_new_files(
   task_id, directory
)
```

---
The function for adding new files to the specified directory.


**Args**

* **directory** (str) : The directory specifiying the location for adding new files.


----


### add_default_label
```python
.add_default_label(
   task_id, default_label
)
```

---
The function for adding a default label to a database and links the label to a given task.


**Args**

* **task_id** (int) : The task's unique identifier.
* **default_label** (string) : The category name of an object.


----


### get_items_names
```python
.get_items_names(
   query, table
)
```

---
The function for getting the items names.


**Args**

* **query** (query) : The query for searching the items.
* **table** (class) : The table for checking the items.


**Returns**

* **list**  : The set list of items.


----


### process_save_dicom_file
```python
.process_save_dicom_file(
   file_data, directory, filename
)
```

---
Processes and saves the uploaded DICOM file.


**Args**

* **file_data** (FileStorage) : The DICOM file data.
* **directory** (str) : The directory for saving the DICOM file.
* **filename** (str) : The name of the DICOM file.


----


### process_save_video_file
```python
.process_save_video_file(
   file_data, directory, filename, task_id
)
```

---
Processes video file and saves frames in JPG format.


**Args**

* **file_data** (FileStorage) : The MP4 file data.
* **directory** (str) : The directory for saving the frames.
* **filename** (str) : The name of the MP4 file.
* **task_id** (int) : The unique task identifier.


----


### process_save_seq_file
```python
.process_save_seq_file(
   file_data, directory, filename, camera, frames
)
```

---
Processes sequence file and saves frames in PNG format


**Args**

* **file_data** (FileStorage) : The SEQ file data.
* **directory** (str) : The directory for saving the frames.
* **filename** (str) : The name of the SEQ file.
* **camera** (str) : the type of camera.
* **frames** (int) : the number specifing the frequency of saving frames.


----


### make_directories
```python
.make_directories(
   directory_files, directory_annotations
)
```

---
The function for creating directories for annotations and files storage.


**Args**

* **directory** (str) : The directory for files location.
* **directory_annotations** (str) : The directory for annotations location.


----


### remove_directory
```python
.remove_directory(
   directory
)
```

---
The function for removing the specified directory.


**Args**

* **directory** (str) : The directory to be removed.


----


### remove_db_task_data
```python
.remove_db_task_data(
   task_id
)
```

---
The function for removing data associated with a given task.


**Args**

* **task_id** (int) : The unique task identifier.

