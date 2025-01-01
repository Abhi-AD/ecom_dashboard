from django.urls import path
from apps.expenses.views import (
    index,
    add_expense,
    expense_edit,
    expense_delete,
    search_expenses,
)

urlpatterns = [
    path("", index, name="index"),
    path("add-expense/", add_expense, name="add_expense"),
    path("expense-edit/<int:id>/", expense_edit, name="expense_edit"),
    path("expense-delete/<int:id>/", expense_delete, name="expense_delete"),
    path("search-expense/", search_expenses, name="search_expenses"),
]
