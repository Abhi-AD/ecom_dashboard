from django.urls import path
from apps.authentication.views import RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="registration"),
]
