from django.urls import path
from apps.expenses.views import (
    index,
    add_expense,
    expense_edit,
    expense_delete,
    search_expenses,
    expense_category_summary,
    stats_view,
    export_csv,
)

urlpatterns = [
    path("", index, name="index"),
    path("add-expense/", add_expense, name="add_expense"),
    path("expense-edit/<int:id>/", expense_edit, name="expense_edit"),
    path("expense-delete/<int:id>/", expense_delete, name="expense_delete"),
    path("search-expense/", search_expenses, name="search_expenses"),
    path("stats/", stats_view, name="stats"),
    path("export-csv/", export_csv, name="export_csv"),
    path(
        "expense-category-summary/",
        expense_category_summary,
        name="expense_category_summary",
    ),
]
