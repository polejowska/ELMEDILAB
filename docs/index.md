# ELMEDILAB
*Medical labeling software for machine learning*
<img src="logo.gif">
### Table of contents

- [1. Overview](#1-overview) <!-- omit in toc -->
  - [1.1. About the project](#11-about-the-project)
  - [1.2. Key features](#12-key-features)
  - [1.3. Technology stack](#13-technology-stack)
  - [1.4. Project summary information](#14-project-summary-information)
- [2. Application](#2-application)
  - [2.1. Requirements](#21-requirements)
  - [2.2. Run the application](#22-run-the-application)
- [3. Documentation](#3-documentation)
- [4. Automatic tests](#4-automatic-tests)

### 1. Overview
#### 1.1. About the project

<p>The project consists of fully-featured web application which main purpose is to allow proper users to label medical images. The application gathers created annotations in order to use them for developing machine learning algorithms that require qualitative and meaningful data. <br> This software was evaluated by proper tests and System Usability Scale which estimated that the application is characterized by a high degree of usability.</p>

#### 1.2. Key features

|  |  |
| :--- | --- |
| Labeling visualized images | Bounding box type annotation generation  |
| Multiple types of files supported | DICOM, SEQ (thermal imaging FLIR cameras models: SC3000, A655SC, A320G), MP4, PNG, JPEG, JPG, BMP  |
| Exporting annotations | PASCAL VOC XML, COCO JSON, YOLO TXT  |
| Converting annotations formats | PASCAL VOC XML -> COCO JSON, PASCAL VOC XML -> YOLO TXT, COCO JSON -> YOLO TXT  |
| Additional | Managing users, managing submitted annotations, managing tasks and files within a given task  |

Features availability differ for the normal user. The administrator has wider range of available features.

#### 1.3. Technology stack

|  |  |
| --- | --- |
| Python | Server-side role for processing the application data. |
| Flask | Web microframework - handling routes, requests and responses. |
| Jinja2 | Template engine for dynamic content loading. |
| HTML5 | Client-side role for web pages construction. |
| JavaScript | Client-side role for interacting with the application web pages. |
| CSS, Bootstrap | Styling and designing repsonsive web pages. |

#### 1.4. Project summary information

##### Main Languages
| LANGUAGE | FILES | CODE LINES | COMMENT LINES | BLANK LINES | TOTAL LINES |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Python | 33 | 2,038 | 830 | 463 | 3,331 |
| HTML + JavaScript | 33 | 2,204 | 0 | 127 | 2,331 |
| CSS | 4 | 487 | 7 | 88 | 582 |
| XML | 1 | 27 | 0 | 0 | 27 |

##### Directories
|  | FILES | CODE LINES | COMMENT LINES | BLANK LINES | TOTAL LINES |
| :--- | ---: | ---: | ---: | ---: | ---: |
| export_convert | 4 | 560 | 160 | 105 | 825 |
| task | 4 | 297 | 127 | 66 | 490 |
| labeling | 3 | 300 | 123 | 60 | 483 |
| seq_processing | 4 | 193 | 69 | 51 | 313 |
| admin | 3 | 149 | 67 | 37 | 253 |
| user | 4 | 133 | 54 | 30 | 217 |
| auth | 3 | 129 | 22 | 20 | 171 |
| main | 2 | 14 | 3 | 10 | 27 |
| errors | 2 | 14 | 32 | 12 | 58 |
| templates | 34 | 2,231 | 0 | 127 | 2,358 |
| static | 4 | 487 | 7 | 88 | 582 |
|  | 71 | 4,762 | 844 | 681 | 6,287 |

### 2. Application
#### 2.1. Requirements

All the requirements are included in this project in the following files: requirements.txt, Pipfile, Pipfile.lock.

Administrator credentials: 
* login: admin
* email: admin@admin.com
* password: administrator

#### 2.2. Run the application

In the main project directory, in the command line, run the following commands:

`pipenv shell`<br>

`pipenv run app.y`

Navigate to the http://127.0.0.1:5000 in the browser.

Alternatively, the application can be run from the ELEMDILAB/app.py file (recommended for development purposes).

### 3. Documentation

In order to get access to the prepared project documentation where all the functions included in this project are properly explained,
navigate to the project's root directory (\ELMEDILAB) and in the command line run:

`pipenv shell`

`pipenv run mkdocs serve`

Navigate to the http://127.0.0.1:8000 in the browser.


### 4. Automatic tests

Running prepared tests is possible by navigating to the project's root directory (\ELMEDILAB) and entering in the command line the following command:

`pytest`
<br>

The test raport is available in the /tests/results/pytest_report.html file.
<br>


<br>
Author: Agata Polejowska, Gdansk University of Technology
<br>