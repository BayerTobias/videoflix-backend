from rest_framework.test import APITestCase
from django.urls import reverse
from djoser.utils import encode_uid
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


class TestSetup(APITestCase):
    def setUp(self):
        self.token_login_url = reverse("login")
        self.token_logout_url = reverse("logout")
        self.user_create_url = reverse("user-list")
        self.user_activate_url = reverse("user-activation")
        self.user_resend_activation_url = reverse("user-resend-activation")
        self.user_set_password_url = reverse("user-set-password")
        self.user_reset_password_url = reverse("user-reset-password")
        self.user_reset_password_confirm_url = reverse("user-reset-password-confirm")
        self.user_set_username_url = reverse("user-set-username")
        self.user_reset_username_url = reverse("user-reset-username")
        self.user_reset_username_confirm_url = reverse("user-reset-username-confirm")
        self.user_me_url = reverse("user-me")
        self.user_delete_url = reverse("user-detail", kwargs={"pk": 1})

        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "re_password": "testpassword123",
        }

        # Create user
        self.client.post(self.user_create_url, self.user_data, format="json")

        # Activate user
        user = User.objects.get(email=self.user_data["email"])
        uid = encode_uid(user.pk)
        token = default_token_generator.make_token(user)
        data = {"uid": uid, "token": token}
        self.client.post(self.user_activate_url, data, format="json")

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
