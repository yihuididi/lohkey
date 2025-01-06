from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

@login_required
def home(request):
    # Retrieve the Google UID for the currently logged-in user
    social_account = SocialAccount.objects.filter(user=request.user, provider="google").first()
    google_user_id = social_account.uid if social_account else None

    return render(request, "home.html", {"google_user_id": google_user_id})

def logout_view(request):
    logout(request)
    return redirect("/")

def portfolio_view(request):
    return render(request, "portfolio.html")

def risk_management_view(request):
    return render(request, "risk-management.html")

def risk_advice_view(request):
    return render(request, "risk-advice.html")

 
