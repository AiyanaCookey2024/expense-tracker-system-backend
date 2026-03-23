from rest_framework.routers import DefaultRouter
from .views import SalaryPeriodView, ExpenseView, BudgetView

router = DefaultRouter()
router.register(r'salary-periods', SalaryPeriodView, basename='salary-period')
router.register(r'expenses', ExpenseView, basename='expense')
router.register(r'budgets', BudgetView, basename='budget')

urlpatterns = router.urls
