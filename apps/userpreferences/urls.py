from django.urls import path
from apps.userpreferences.views import index

urlpatterns = [
    path("", index, name="preferences"),
]
