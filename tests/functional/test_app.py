from website import create_app
from website.config import TestingConfig

from unittest import TestCase
from website import create_app, db
from website.config import TestingConfig


class FunctionalTestWebApp(TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_site.db'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['LOGIN_DISABLED'] = True
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_home_page_redirect(self):
        response = self.client.get('/', follow_redirects=True)
        assert response.status_code == 200
        # assert response.request.path == '/login'

    def test_pages(self):
        assert self.client.get('/request-access').status_code == 200
        assert self.client.get('/user-admin').status_code == 200
        assert self.client.get('/help').status_code == 200
        assert self.client.get('/admin/manage-tasks').status_code == 302

    def test_request(self):
        response = self.client.post('/request-access',
            data = dict(username="test_user", email="test@gmail.com", password="test", form=""),
            follow_redirects=True
        )
        self.assertIn(b'request', response.data)

    def test_404(self):
        rv = self.client.get('/other')
        self.assertEqual(rv.status, '404 NOT FOUND')