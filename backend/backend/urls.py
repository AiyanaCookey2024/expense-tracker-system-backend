from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from expenses import views


router = routers.DefaultRouter()
router.register(r'expenses', views.ExpenseView, 'expense')
router.register(r'salary-periods', views.SalaryPeriodView, 'salary-period')
router.register(r'budgets', views.BudgetView, 'budget')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('authentication.urls')),
]
