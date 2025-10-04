from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

URL_LOGIN = "/login/"
URL_HOME_ADMIN = "/home_admin/"
URL_HOME_USER = "/home_empleado/"

class LoginAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username="0914",
            email="milimantilla06@gmail.com",
            password="0914"
        )

    def test_admin_login_con_username_redirige_a_home(self):
        resp = self.client.post(URL_LOGIN, {
            "usuario": "0914",
            "contrasena": "0914"
        }, follow=True)
        redirige = any(URL_HOME_ADMIN in url for (url, code) in resp.redirect_chain)
        self.assertTrue(redirige, "El admin debería redirigir a /home_admin/")

    def test_admin_login_con_email_no_aplica(self):
        resp = self.client.post(URL_LOGIN, {
            "usuario": "milimantilla06@gmail.com",
            "contrasena": "0914"
        }, follow=True)
        redirige = any(URL_HOME_ADMIN in url for (url, code) in resp.redirect_chain)
        self.assertFalse(redirige, "Para admin, login con email NO debe redirigir a /home_admin/")

class LoginOperadorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.operador = User.objects.create_user(
            username="operador",
            email="operador@example.com",
            password="1234",
            is_active=True
        )

    def test_operador_login_con_username_redirige_a_home(self):
        resp = self.client.post(URL_LOGIN, {
            "usuario": "operador",
            "contrasena": "1234"
        }, follow=True)
        redirige = any(URL_HOME_USER in url for (url, code) in resp.redirect_chain)
        self.assertTrue(redirige, "Operador debería redirigir a /home_empleado/")

    def test_operador_login_con_email_según_requisito(self):
        """
        Este test representa el REQUISITO (que los usuarios entren con email).
        Hoy va a fallar → evidencia de bug.
        """
        resp = self.client.post(URL_LOGIN, {
            "usuario": "operador@example.com",
            "contrasena": "1234"
        }, follow=True)
        redirige = any(URL_HOME_USER in url for (url, code) in resp.redirect_chain)
        self.assertTrue(redirige, "REQ: login con email debería funcionar (bug actual)")
