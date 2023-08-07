import tornado.testing
from tornado_sqlalchemy import SQLAlchemy
from main import Application


DATABASE_URL = 'sqlite:///:memory:'


class RegisterTest(tornado.testing.AsyncHTTPTestCase):
    request_body = b'{"name": "Teste Python", "email": "cai11o10@teste.com", "password": "ASDaAAD@233", "password2": "ASDaAAD@233"}'  # noqa

    def get_app(self):
        self.db = SQLAlchemy(url=DATABASE_URL)
        return Application()

    def setUp(self):
        super(RegisterTest, self).setUp()
        self.db.create_all()

    def tearDown(self):
        self.db.drop_all()
        super(RegisterTest, self).tearDown()

    def test_register_user(self):
        response = self.fetch('/api/v1/register', method='POST', body=self.request_body)  # noqa
        self.assertEqual(response.code, 200)

    def test_login_user(self):
        request_body = b'{"email": "cai1o10@teste.com", "password": "Caiokaiak@1"}'  # noqa
        response = self.fetch('/api/v1/login', method='POST', body=request_body)  # noqa
        self.assertEqual(response.code, 200)

    def test_register_existing_user(self):
        self.fetch('/ap1/v1/register', method='POST', body=self.request_body)

        response = self.fetch('/ap1/v1/register', method='POST', body=self.request_body)  # noqa
        self.assertEqual(response.code, 400)
        self.assertIn("Usuário já existe", response.body.decode())
