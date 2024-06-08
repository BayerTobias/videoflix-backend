from .test_setup import TestSetup
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from djoser.utils import encode_uid


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

    def test_login_with_wrong_password(self):
        login_data = {
            "username": self.user_data["username"],
            "password": "wrongPassword123",
        }
        response = self.client.post(self.token_login_url, login_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_get_user_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, 200)

    def test_update_user_information(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        user_data = {
            "username": "testuser123",
            "first_name": "test",
            "last_name": "user",
        }
        response = self.client.patch(self.user_me_url, user_data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_get_user_data_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {' '}")
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Invalid token header", response.content)

    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        response = self.client.post(self.token_logout_url, {}, fromat="json")
        self.assertEqual(response.status_code, 204)

    def test_delete_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.auth_token}")
        user_delete_url = reverse("user-detail", kwargs={"pk": self.user.pk})
        body = {"current_password": self.user_data.get("password")}
        response = self.client.delete(user_delete_url, body, format="json")
        self.assertEqual(response.status_code, 204)

    def test_request_password_reset_mail(self):
        body = {"email": self.user_data.get("email")}
        response = self.client.post(self.user_reset_password_url, body, format="json")
        self.assertEqual(response.status_code, 204)

    def test_password_reset(self):
        # Request password reset
        body = {"email": self.user_data.get("email")}
        request_response = self.client.post(
            self.user_reset_password_url, body, format="json"
        )
        self.assertEqual(request_response.status_code, 204)

        # Generate token and UID
        user = User.objects.get(email=self.user_data.get("email"))
        uid = encode_uid(user.pk)
        token = default_token_generator.make_token(user)

        # set new Password
        reset_data = {
            "uid": uid,
            "token": token,
            "new_password": "newtestpassword123",
        }

        reset_response = self.client.post(
            self.user_reset_password_confirm_url, reset_data, format="json"
        )
        self.assertEqual(reset_response.status_code, 204)

        user.refresh_from_db()
        self.assertTrue(user.check_password("newtestpassword123"))
