from django.contrib.auth.models import User 
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch 

from authentication.models import PasswordResetToken
from expenses.models import SalaryPeriod

class AuthenticationTests(APITestCase):
    def test_register_user(self):
        response = self.client.post(
            "/api/auth/register/",
            {
                "username": "aiyana",
                "email": "aiyana@gmail.com",
                "password": "Password123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertTrue(User.objects.filter(username="aiyana").exists())

    def test_login_valid_credentials(self):
        User.objects.create_user(
            username="aiyana",
            email="aiyana@gmail.com",
            password="Password123!",
        )

        response = self.client.post(
            "/api/auth/token/",
            {
                "username": "aiyana",
                "password": "Password123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        User.objects.create_user(
            username="aiyana",
            email="aiyana@gmail.com",
            password="Password123!"
        )

        response = self.client.post(
            "/api/auth/token/",
            {
                "username": "aiyana",
                "password": "WrongPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# This stops real emails sending in tests
    @patch("authentication.views.SendGridAPIClient")
    def test_password_reset_request_existing_email(self, mock_sendgrid):
        User.objects.create_user(
            username="Aiyana1",
            email="aiyana1@gmail.com",
            password="OldPassword123!",
        )

        mock_sendgrid.return_value.send.return_value.status_code = 202
    
        response = self.client.post(
            "/api/auth/password-reset/",
            {"email": "aiyana1@gmail.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            PasswordResetToken.objects.filter(user__email="aiyana1@gmail.com").exists()
        )

    def test_password_reset_request_nonexistent_email(self):
        response = self.client.post(
            "/api/auth/password-reset/",
            {"email": "noaiayana@gmail.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"],
            "If email exists, reset link sent",
        )

    def test_password_reset_confirm_valid_token(self):
        user = User.objects.create_user(
            username="resetaiyana",
            email="resetaiyana@gmail.com",
            password="OldPassword123!",
        )

        token_obj = PasswordResetToken.objects.create(user=user)

        response = self.client.post(
            "/api/auth/password-reset-confirm/",
            {
                "token": str(token_obj.token),
                "new_password": "NewPassword123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertTrue(user.check_password("NewPassword123!"))
        self.assertFalse(
            PasswordResetToken.objects.filter(token=str(token_obj.token)).exists()
        )

    def test_password_reset_confirm_invalid_token(self):
        response = self.client.post(
            "/api/auth/password-reset-confirm/",
            {
                "token": "invalid-token",
                "new_password": "NewPassword123!"
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Invalid token")
    
    def test_password_reset_token_cannot_be_reused(self):
        user = User.objects.create_user(
            username="reuseuser",
            email="reuse@gmail.com",
            password="OldPassword123!",
        )

        token_obj = PasswordResetToken.objects.create(user=user)

        first_response = self.client.post(
            "/api/auth/password-reset-confirm/",
            {
                "token": str(token_obj.token),
                "new_password": "NewPassword123!",
            },
            format="json",
        )

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)

        second_response = self.client.post(
            "/api/auth/password-reset-confirm/",
            {
                "token": str(token_obj.token),
                "new_password": "AnotherPassword123!",
            },
            format="json",
        )

        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
    
    @patch("authentication.views.SendGridAPIClient")
    def test_password_reset_flow_end_to_end(self, mock_sendgrid):
        user = User.objects.create_user(
            username="flowuser",
            email="flowuser@gmail.com",
            password="OldPassword123!",
        )

        mock_sendgrid.return_value.send.return_value.status_code = 202

        reset_request_response = self.client.post(
            "/api/auth/password-reset/",
            {"email": "flowuser@gmail.com"},
            format="json",
        )

        self.assertEqual(reset_request_response.status_code, status.HTTP_200_OK)

        token_obj = PasswordResetToken.objects.get(user=user)

        reset_confirm_response = self.client.post(
            "/api/auth/password-reset-confirm/",
            {
                "token": str(token_obj.token),
                "new_password": "NewPassword123!",
            },
            format="json",
        )

        self.assertEqual(reset_confirm_response.status_code, status.HTTP_200_OK)

        login_response = self.client.post(
            "/api/auth/token/",
            {
                "username": "flowuser",
                "password": "NewPassword123!",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)