from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.choices.positions import Positions
from apps.users.models import User


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.protected_url = reverse("protected-data")

        self.registration_data = {
            "username": "test_tenant",
            "first_name": "Anna",
            "last_name": "Tester",
            "email": "test_tenant@example.com",
            "password": "VioletRiver_2026!",
            "re_password": "VioletRiver_2026!",
        }

    def create_user(self):
        return User.objects.create_user(
            email="existing@example.com",
            password="VioletRiver_2026!",
            username="existing_user",
            first_name="Existing",
            last_name="User",
        )

    def test_user_can_register(self):
        response = self.client.post(
            self.register_url,
            self.registration_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.get(email="test_tenant@example.com")

        self.assertEqual(user.position, Positions.USER.name)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password("VioletRiver_2026!"))

        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertTrue(response.cookies["access_token"]["httponly"])
        self.assertTrue(response.cookies["refresh_token"]["httponly"])

    def test_registration_cannot_assign_admin_position(self):
        data = self.registration_data.copy()
        data["position"] = "ADMIN"

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="test_tenant@example.com")

        self.assertEqual(user.position, Positions.USER.name)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_registration_rejects_different_passwords(self):
        data = self.registration_data.copy()
        data["re_password"] = "DifferentPassword_2026!"

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("password", response.data)

    def test_registration_rejects_duplicate_user(self):
        self.client.post(
            self.register_url,
            self.registration_data,
            format="json",
        )

        response = self.client.post(
            self.register_url,
            self.registration_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    def test_user_can_login_with_email(self):
        self.create_user()

        response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": "VioletRiver_2026!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)
        self.assertTrue(response.cookies["access_token"]["httponly"])
        self.assertTrue(response.cookies["refresh_token"]["httponly"])

    def test_login_rejects_invalid_password(self):
        self.create_user()

        response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": "WrongPassword_2026!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            "Invalid credentials",
        )
        self.assertNotIn("access_token", response.cookies)
        self.assertNotIn("refresh_token", response.cookies)

    def test_protected_endpoint_requires_authentication(self):
        response = self.client.get(self.protected_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_login_cookie_allows_access_and_logout_removes_access(self):
        user = self.create_user()

        login_response = self.client.post(
            self.login_url,
            {
                "email": "existing@example.com",
                "password": "VioletRiver_2026!",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        protected_response = self.client.get(self.protected_url)

        self.assertEqual(protected_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            protected_response.data["user"],
            user.username,
        )

        logout_response = self.client.post(self.logout_url)

        self.assertEqual(
            logout_response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(
            logout_response.cookies["access_token"]["max-age"],
            0,
        )
        self.assertEqual(
            logout_response.cookies["refresh_token"]["max-age"],
            0,
        )

        protected_after_logout = self.client.get(self.protected_url)

        self.assertEqual(
            protected_after_logout.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
