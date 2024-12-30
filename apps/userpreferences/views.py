from django.shortcuts import render
import os, json, pdb
from django.conf import settings
from apps.userpreferences.models import UserPreference
from django.contrib import messages


# Create your views here.
def index(request):
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, "currencies.json")
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        for name, value in data.items():
            currency_data.append({"name": name, "value": value})
    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preference = None
    if exists:
        user_preference = UserPreference.objects.get(user=request.user)
    if request.method == "GET":
        return render(
            request,
            "userpreferences/index.html",
            {"currencies": currency_data, "user_preference": user_preference},
        )
    else:
        currency = request.POST["currency"]
        if exists:
            user_preference.currency = currency
            user_preference.save()
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, "Change currency")
        return render(
            request,
            "userpreferences/index.html",
            {"currencies": currency_data, "user_preference": user_preference},
        )
