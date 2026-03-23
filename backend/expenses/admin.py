from django.contrib import admin
from .models import Expense, Budget, SalaryPeriod


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category')


# Register your models here.
admin.site.register(Budget)
admin.site.register(SalaryPeriod)
admin.site.register(Expense, ExpenseAdmin)