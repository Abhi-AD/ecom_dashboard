from django.urls import path
from apps.authentication.views import RegistrationView, UsernameValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="registration"),
    path(
        "validate-username/",
        csrf_exempt(UsernameValidationView.as_view()),
        name="validate-username",
    ),
]
