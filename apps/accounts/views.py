from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomLoginView(LoginView):

    template_name = "accounts/login.html"

    redirect_authenticated_user = True


def logout_view(request):

    logout(request)

    return redirect("login")