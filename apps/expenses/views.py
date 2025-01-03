from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.expenses.models import Expense, Category
from apps.userpreferences.models import UserPreference
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import json, datetime, csv, xlwt
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# Create your views here.
def search_expenses(request):
    if request.method == "POST":
        try:
            search_str = json.loads(request.body).get("searchText")
            query = (
                Q(amount__startswith=search_str)
                | Q(date__startswith=search_str)
                | Q(category__startswith=search_str)
                | Q(description__icontains=search_str)
            )
            expenses = Expense.objects.filter(query, owner=request.user)
            data = list(expenses.values())
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required(login_url="/auth/login")
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        user_preference = UserPreference.objects.get(user=request.user)
        currency = user_preference.currency
    except UserPreference.DoesNotExist:
        currency = "USD"
    context = {
        "expenses": expenses,
        "categories": categories,
        "page_obj": page_obj,
        "currency": currency,
    }
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
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
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


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 6)
    expenses = Expense.objects.filter(
        owner=request.user, date__gte=six_months_ago, date__lte=todays_date
    )
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filter_by_category = expenses.filter(category=category)
        for item in filter_by_category:
            amount += item.amount
        return amount

    for expense in expenses:
        print("Amount", expense)
        for category in category_list:
            finalrep[category] = get_expense_category_amount(category)
    return JsonResponse({"expense_category_date": finalrep}, safe=False)


def stats_view(request):
    return render(request, "expense/stats.html")


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        "attachment; filename=export" + str(datetime.datetime.now()) + ".csv"
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "Amount",
            "Description",
            "Category",
            "Date",
        ]
    )
    expense = Expense.objects.filter(owner=request.user)
    for exp in expense:
        writer.writerow([exp.amount, exp.description, exp.category, exp.date])
    return response


def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=export" + str(datetime.datetime.now()) + ".xls"
    )
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("Expense")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Amount", "Description", "Category", "Date"]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    row = Expense.objects.filter(owner=request.user).values_list(
        "amount", "description", "category", "date"
    )
    for row_data in row:
        row_num += 1
        for col_num in range(len(row_data)):
            ws.write(row_num, col_num, str(row_data[col_num]), font_style)
    wb.save(response)
    return response
