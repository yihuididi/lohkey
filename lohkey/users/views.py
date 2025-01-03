from django.shortcuts import render,redirect
from django.contrib.auth import logout

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def portfolio_view(request):
    return render(request, "portfolio.html")

def risk_management_view(request):
    return render(request, "risk-management.html")

def risk_advice_view(request):
    return render(request, "risk-advice.html")

 
