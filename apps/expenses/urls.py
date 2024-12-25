from django.urls import path
from apps.expenses.views import index, add_expense

urlpatterns = [
    path("", index, name="index"),
    path("add-expense/", add_expense, name="add_expense"),
]
