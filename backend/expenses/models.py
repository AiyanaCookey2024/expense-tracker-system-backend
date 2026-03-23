from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - £{self.month}/{self.year}"


class SalaryPeriod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('month', 'year')

    def __str__(self):
        return f"{self.month}/{self.year} - £{self.total_salary}"

class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('FOOD', 'Food'),
        ('TRANSPORT','Transport'),
        ('ENTERTAINMENT', 'Entertainment'),
        ('BILLS', 'Bills'),
        ("FUN","Fun"),
        ("MAINTENANCE","Maintenance"),
        ("SAVINGS/INVESTMENTS","Savings/Investments"),
        ('OTHER', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    salary_period = models.ForeignKey(SalaryPeriod, on_delete=models.CASCADE, related_name='expenses')


    def __str__(self):
        return f"{self.title} - £{self.amount}"