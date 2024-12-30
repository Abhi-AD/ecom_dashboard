from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.expenses.models import Expense, Category
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator


# Create your views here.
@login_required(login_url="/auth/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    context = {"expenses": expenses, "categories": categories, "page_obj": page_obj}
    return render(request, "expense/index.html", context)


def add_expense(request):
    categories = Category.objects.all()
    context = {"categories": categories, "values": request.POST}
    if request.method == "GET":
        return render(request, "expense/add-expenses.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expense/add-expenses.html", context)
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expense/add-expenses.html", context)
        Expense.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
        )
        messages.success(request, "Expense added successfully")
        return redirect("index")


def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    date_value = datetime(2024, 12, 30).strftime("%Y-%m-%d")
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
        "date_value": date_value,
    }
    if request.method == "GET":
        return render(request, "expense/edit-expenses.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expense/edit-expenses.html", context)
        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expense/edit-expenses.html", context)
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()
        messages.success(request, "Expense Update successfully")
        return redirect("index")


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect("index")
