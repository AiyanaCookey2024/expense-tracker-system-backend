from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import ExpenseSerializer, SalaryPeriodSerializer, BudgetSerializer
from .models import Expense, SalaryPeriod, Budget


# Create your views here.
class BudgetView(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SalaryPeriodView(viewsets.ModelViewSet):
    serializer_class = SalaryPeriodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SalaryPeriod.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseView(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)