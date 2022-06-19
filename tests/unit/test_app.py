import shutil
from unittest import TestCase
import unittest
from flask import current_app
from werkzeug.datastructures import FileStorage

from website import create_app, db
from website.config import TestingConfig
from website.export_convert.forms import ConvertForm, ExportForm
from website.labeling.utils import get_saved_labels
from website.models import ACCESS, Annotation, Request, Task, User

from website.auth.forms import RequestForm, LoginForm
from website.task.forms import CreateTaskForm, TaskForm
from website.task.utils import check_extension as check_upload_extension, process_save_dicom_file, process_save_seq_file
from website.export_convert.utils import check_extension as check_label_extension, convert_bbox_coco_to_yolo, convert_xml_to_json

import os, io
from os import walk

from website.user.forms import UpdateAccountForm


TEST_FILES_DIRECTORY = 'tests\\examples_after_test\\'

class UnitTestWebApp(TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_site.db'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()
        os.mkdir(TEST_FILES_DIRECTORY)

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None
        shutil.rmtree(TEST_FILES_DIRECTORY)

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app
    
    def test_request_user_model(self):
        request = Request(
            username='test', 
            email='test@test.com',
            password='test'
            )

        db.session.add(request)
        db.session.commit()

        assert request.username == 'test'
        assert request.email == 'test@test.com'
        assert request.password != 'test'
        assert request.approved == False

        request.approved = True

        user = User(
            username=request.username,
            email=request.email,
            password=request.password
            )

        db.session.add(user)
        db.session.commit()

        assert user.username == request.username
        assert user.email == request.email
        assert user.password == request.password
        assert user.access == ACCESS['user']

        assert Request.query.count() == 1
        assert User.query.count() == 1

    def test_instantiate_form(self):

        with self.app.test_request_context('/'):
            form = RequestForm()
        self.assertIsInstance(form, RequestForm)

        with self.app.test_request_context('/'):
            form = LoginForm()
        self.assertIsInstance(form, LoginForm)

        with self.app.test_request_context('/'):
            form = ExportForm()
        self.assertIsInstance(form, ExportForm)
    
        with self.app.test_request_context('/'):
            form = ConvertForm()
        self.assertIsInstance(form, ConvertForm)

        with self.app.test_request_context('/'):
            form = CreateTaskForm()
        self.assertIsInstance(form, CreateTaskForm)

        with self.app.test_request_context('/'):
            form = TaskForm()
        self.assertIsInstance(form, TaskForm)

        with self.app.test_request_context('/'):
            form = UpdateAccountForm()
        self.assertIsInstance(form, UpdateAccountForm)

    def test_process_seq_file_SC3000(self):
        files_path = 'tests\\examples\\SC3000\\'
        filenames = next(walk(files_path), (None, None, []))[2]
        for filename in filenames:
            with open(os.path.join(files_path, filename), 'rb') as fh:
                buf = io.BytesIO(fh.read())
                mock_file = FileStorage(
                    stream=buf,
                    filename=filename,
                    content_type="application/octet-stream",
                    )
                process_save_seq_file(mock_file, TEST_FILES_DIRECTORY, filename, 'SC3000', 100)
            assert os.path.exists(TEST_FILES_DIRECTORY + 'SC3000_' + filename + '_frame_0_16bits.png'), "SEQ file processed and saved for display successfully"

    def test_process_seq_file_A655SC(self):
        files_path = 'tests\\examples\\A655SC'
        filenames = next(walk(files_path), (None, None, []))[2]
        for filename in filenames:
            with open(os.path.join(files_path, filename), 'rb') as fh:
                buf = io.BytesIO(fh.read())
                mock_file = FileStorage(
                    stream=buf,
                    filename=filename,
                    content_type="application/octet-stream",
                    )
                process_save_seq_file(mock_file, TEST_FILES_DIRECTORY, filename, 'A655SC', 1000)
            assert os.path.exists(TEST_FILES_DIRECTORY + filename + '_A655SC_frame_1.png'), "SEQ file processed and saved for display successfully"

    def test_process_seq_file_A320G(self):
        files_path = 'tests\\examples\\A320G'
        filenames = next(walk(files_path), (None, None, []))[2]
        for filename in filenames:
            with open(os.path.join(files_path, filename), 'rb') as fh:
                buf = io.BytesIO(fh.read())
                mock_file = FileStorage(
                    stream=buf,
                    filename=filename,
                    content_type="application/octet-stream",
                    )
                process_save_seq_file(mock_file, TEST_FILES_DIRECTORY, filename, 'A320G', 100)
            assert os.path.exists(TEST_FILES_DIRECTORY + filename + '_A320G_frame_1.png'), "SEQ file processed and saved for display successfully"

    def test_process_dicom_file(self):
        with open('tests\\examples\\DICOM\\CT_small.dcm', 'rb') as fh:
            buf = io.BytesIO(fh.read())
            mock_file = FileStorage(
                stream=buf,
                filename="CT_small.dcm",
                content_type="application/octet-stream",
                )
            process_save_dicom_file(mock_file, TEST_FILES_DIRECTORY, 'CT_small.dcm')
        assert os.path.exists('tests\\examples_after_test\\CT_small.dcm'), "DICOM file processed and saved for display successfully"

    def test_labels(self):
        assert get_saved_labels(task_id=0, filename='example') == []

        task = Task(id=2, name='TestTask')

        db.session.add(task)
        db.session.commit()

        annotation = Annotation(
            name='TestAnnotation', 
            filename='TestFilename', 
            nr=1, 
            task_id=2, 
            creator='TestCreator', 
            pose='', 
            truncated='', 
            difficult='1', 
            occluded='0', 
            x_max=30, 
            y_max=30, 
            y_min=20, 
            x_min=0
         )

        db.session.add(annotation)
        db.session.commit()

        saved_labels = get_saved_labels(task_id=2, filename='TestFilename')
        saved_label = saved_labels[0]

        assert saved_labels != []
        assert saved_label.x_min < saved_label.x_max
        assert saved_label.y_min < saved_label.y_max

    def test_convert_labels(self):
        bbox = [100, 100, 100, 100]
        img_width, img_height = 700, 1000
        x, y, w, h = convert_bbox_coco_to_yolo(bbox, img_width, img_height)

        assert x < img_width and x < 1 and x > 0
        assert y < img_height and y < 1 and y > 0
        assert w < img_width and w < 1 and w > 0
        assert h < img_height and h < 1 and h > 0

    def test_check_upload_extension(self):
        assert check_upload_extension('example.png')
        assert check_upload_extension('example.seq')
        assert check_upload_extension('example.dcm')
        assert check_upload_extension('example.jpg')
        assert check_upload_extension('example.mp4')
        assert check_upload_extension('example.pdf') == False
        assert check_upload_extension('example.zip') == False

    def test_check_label_extension(self):
        assert check_label_extension('annotation.xml')
        assert check_label_extension('annotation.json')
        assert check_label_extension('annotation.txt')
        assert check_label_extension('annotation.doc') == False
        assert check_label_extension('annotation.pdf') == False
