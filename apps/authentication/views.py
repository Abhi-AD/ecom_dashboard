import json
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse
from validate_email import validate_email
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from apps.authentication.utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Create your views here.
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data["email"]
        if not validate_email(email):
            return JsonResponse(
                {"email_error": "Email is not valid"},
                status=400,
            )
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"email_error": "sorry email already exists"},
                status=409,
            )

        return JsonResponse({"email_valid": True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data["username"]
        if not str(username).isalnum():
            return JsonResponse(
                {
                    "username_error": "username should only contain alphanumeric characters "
                },
                status=400,
            )
        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"username_error": "sorry username already exists"},
                status=409,
            )

        return JsonResponse({"username_valid": True})


class RegistrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")

    def post(self, request):
        # get user data from registration, validate, create
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        context = {"fieldValues": request.POST}
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(
                        request, "Password must be at least 6 characters long."
                    )
                    return render(request, "authentication/register.html", context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                uidb64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
                domain = get_current_site(request).domain
                link = reverse(
                    "activate",
                    kwargs={
                        "uidb64": uidb64,
                        "token": token_generator.make_token(user),
                    },
                )
                activate_link = "http://" + domain + link
                email_subject = "Activate your account"
                email_body = (
                    f"Hi {user.username},\n\n"
                    f"Please use this link to verify your account:\n{activate_link}\n\n"
                    "Thank you for registering with us!"
                )
                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=False)
                messages.success(request, "Account successfully created")
                return render(request, "authentication/register.html")

        return render(request, "authentication/register.html")


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect("login" + "?message=" + "User already activated")

            if user.is_active:
                return redirect("login")

            user.is_active = True
            user.save()

            messages.success(request, "User account has been activated successfully")
            return redirect("login")

        except Exception as e:
            pass
        return redirect("login")


class LoginView(View):
    def get(self, request):
        return render(request, "authentication/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(
                        request, f"Welcome {user.username}, you are logged in."
                    )
                    return redirect("index")
                messages.error(request, "Account is not activated")
                return render(request, "authentication/login.html")
            messages.error(request, "Invalid credentials")
            return render(request, "authentication/login.html")
        messages.error(request, "Please fill your credentials")
        return render(request, "authentication/login.html")


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, "authentication/reset-password.html")

    def post(self, request):
        email = request.POST.get("email")
        context = {"values": request.POST}

        if not validate_email(email):
            messages.error(request, "Email is not valid")
            return render(request, "authentication/reset-password.html", context)

        user = User.objects.filter(email=email)

        if not user.exists():
            messages.error(request, "No user found with this email address")
            return render(request, "authentication/reset-password.html", context)

        user = user.first()  # Get the first user if there are any matches
        uidb64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
        domain = get_current_site(request).domain
        link = reverse(
            "reset-user-password",
            kwargs={
                "uidb64": uidb64,
                "token": PasswordResetTokenGenerator().make_token(user),
            },
        )
        reset_link = "http://" + domain + link

        email_subject = "Password reset token"
        email_body = (
            f"Hi there,\n\n"
            f"Please use this link to reset your account password:\n{reset_link}\n\n"
            "Thank you for registering with us!"
        )
        email_message = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [email],
        )
        email_message.content_subtype = "html"  # Ensure it sends as HTML email
        email_message.send(fail_silently=False)

        messages.success(request, "We have sent you an email to reset your password")
        return render(request, "authentication/reset-password.html")


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        return render(request, "authentication/set-newpassword.html", context)

    def post(self, request, uidb64, token):
        context = {"uidb64": uidb64, "token": token}
        password = request.POST["password"]
        password2 = request.POST["password2"]
        if password != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "authentication/set-newpassword.html", context)
        if len(password) < 4:
            messages.error(request, "Password should be at least 4 characters long")
            return render(request, "authentication/set-newpassword.html", context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Token is invalid or expired")
                return redirect("request-password")
            user.password = password
            user.set_password(password)
            user.save()         
            messages.success(request, "Password reset successful, you can login again")
            return redirect("login")

        except Exception as e:
            messages.info(request, "Something went wrong")
            return render(request, "authentication/set-newpassword.html", context)
