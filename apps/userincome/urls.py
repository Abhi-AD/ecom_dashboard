from django.urls import path
from apps.userincome.views import (
    index,
    add_userIncome,
    userIncome_edit,
    userIncome_delete,
    search_income,
)

urlpatterns = [
    path("", index, name="income"),
    path("add-income/", add_userIncome, name="add_income"),
    path("income-edit/<int:id>/", userIncome_edit, name="income_edit"),
    path("income-delete/<int:id>/", userIncome_delete, name="income_delete"),
    path("search-income/", search_income, name="search_income"),
]
