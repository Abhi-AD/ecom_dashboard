from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.userincome.models import Source, UserIncome
from apps.userpreferences.models import UserPreference
from django.contrib import messages
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
# Create your views here.
def search_income(request):
    if request.method == "POST":
        try:
            search_str = json.loads(request.body).get("searchText")
            query = (
                Q(amount__startswith=search_str)
                | Q(date__startswith=search_str)
                | Q(source__startswith=search_str)
                | Q(description__icontains=search_str)
            )
            expenses = UserIncome.objects.filter(query, owner=request.user)
            data = list(expenses.values())
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required(login_url="/auth/login")
def index(request):
    sources = Source.objects.all()
    userincome = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(userincome, 10)
    page_number = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        "income": userincome,
        "sources": sources,
        "page_obj": page_obj,
        "currency": currency,
    }
    return render(request, "userincome/index.html", context)


def add_userIncome(request):
    sources = Source.objects.all()
    context = {"sources": sources, "values": request.POST}
    if request.method == "GET":
        return render(request, "userincome/add-userincome.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "userincome/add-userincome.html", context)
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "userincome/add-userincome.html", context)
        UserIncome.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            source=source,
            description=description,
        )
        messages.success(request, "UserIncome added successfully")
        return redirect("income")


def userIncome_edit(request, id):
    userincome = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        "income": userincome,
        "values": userincome,
        "sources": sources,
    }
    if request.method == "GET":
        return render(request, "userincome/edit-userincome.html", context)
    if request.method == "POST":
        amount = request.POST["amount"]
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "userincome/edit-userincome.html", context)
        description = request.POST["description"]
        date = request.POST["income_date"]
        source = request.POST["source"]
        if not description:
            messages.error(request, "Description is required")
            return render(request, "userincome/edit-userincome.html", context)
        userincome.owner = request.user
        userincome.amount = amount
        userincome.date = date
        userincome.source = source
        userincome.description = description
        userincome.save()
        messages.success(request, "UserIncome Update successfully")
        return redirect("income")


def userIncome_delete(request, id):
    userincome = UserIncome.objects.get(pk=id)
    userincome.delete()
    messages.success(request, "UserIncome deleted successfully")
    return redirect("income")
