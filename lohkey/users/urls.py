from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("", views.home),
    path('accounts/login/', lambda request: redirect('socialaccount_login', provider='google')),
    path("logout", views.logout_view),
    path("portfolio", views.portfolio_view),
    path("risk-management", views.risk_management_view),
    path("risk-advice", views.risk_advice_view)
]