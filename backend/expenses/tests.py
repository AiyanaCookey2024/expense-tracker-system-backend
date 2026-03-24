from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from expenses.models import Budget, Expense, SalaryPeriod

class ExpenseTrackerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="aiyana",
            email="aiyana@gmail.com",
            password="Password123!",
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.salary_period = SalaryPeriod.objects.create(
            month=3,
            year=2026,
            total_salary=2500.00
        )
    
    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
    
    def test_protected_budgets_requires_authentication(self):
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_expenses_requires_authentication(self):
        response = self.client.get("/api/expenses/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_budget_authenticated(self):
        self.authenticate()

        response = self.client.post(
            "/api/budgets/",
            {
                "name": "Food",
                "total_amount": "300.00",
                "month": 3, 
                "year": 2026,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Food")
        self.assertEqual(Budget.objects.count(), 1)

    def test_update_budget(self):
        self.authenticate()

        budget = Budget.objects.create(
            name="Transport",
            total_amount="100.00",
            month=3,
            year=2026,
        )

        response = self.client.put(
            f"/api/budgets/{budget.id}/",
            {
                "name": "Transport Updated",
                "total_amount": "120.00",
                "month": 3,
                "year": 2026,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        budget.refresh_from_db()
        self.assertEqual(budget.name, "Transport Updated")

    def test_delete_expense(self):
        self.authenticate()

        expense = Expense.objects.create(
            category="BILLS",
            title="Phone Bill",
            amount="30.00",
            salary_period=self.salary_period,
        )

        response = self.client.delete(f"/api/expenses/{expense.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=expense.id).exists())

    def test_get_salary_periods_authenticated(self):
        self.authenticate()

        response = self.client.get("/api/salary-periods/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_expense_invalid_missing_title(self):
        self.authenticate()

        response = self.client.post(
            "/api/expenses/",
            {
                "category": "FOOD",
                "amount": "12.00",
                "salary_period": self.salary_period.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_journey_login_create_budget_create_expense(self):
        login_response = self.client.post(
            "/api/auth/token/",
            {
                "username": "aiyana",
                "password": "Password123!",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        budget_response = self.client.post(
            "/api/budgets/",
            {
                "name": "Food",
                "total_amount": "300.00",
                "month": 3,
                "year": 2026,
            },
            format="json",
        )
        self.assertEqual(budget_response.status_code, status.HTTP_201_CREATED)

        expense_response = self.client.post(
            "/api/expenses/",
            {
                "category": "FOOD",
                "title": "Groceries",
                "amount": "25.00",
                "salary_period": self.salary_period.id,
            },
            format="json",
        )
        self.assertEqual(expense_response.status_code, status.HTTP_201_CREATED)

        budgets_response = self.client.get("/api/budgets/")
        expenses_response = self.client.get("/api/expenses/")

        self.assertEqual(budgets_response.status_code, status.HTTP_200_OK)
        self.assertEqual(expenses_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(budgets_response.data), 1)
        self.assertGreaterEqual(len(expenses_response.data), 1)
