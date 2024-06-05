from .test_setup import TestSetup
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import decode_uid, encode_uid


class TestAuth(TestSetup):

    def test_user_registration(self):
        user_data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "testpassword123",
            "re_password": "testpassword123",
        }
        response = self.client.post(self.user_create_url, user_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_user_registration_missing_field(self):
        user_data = {
            "username": "testuser2",
            "email": "testuser2@example.com",
        }
        response = self.client.post(self.user_create_url, user_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_user_registration_username_exists(self):
        response = self.client.post(self.user_create_url, self.user_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_activate_user(self):
        user = User.objects.get(email=self.user_data["email"])
        self.assertTrue(user.is_active)

    def test_login(self):
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.token_login_url, login_data, format="json")
        self.assertEqual(response.status_code, 200)
