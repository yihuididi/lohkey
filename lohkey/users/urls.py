from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path("", views.home),
    path('accounts/login/', lambda request: redirect('socialaccount_login', provider='google')),
    path("logout", views.logout_view),
    path("portfolio", views.portfolio_view),
    path("risk-management", views.risk_management_view),
    path("risk-advice", views.risk_advice_view),
    path("submit-wallet-address/", views.submit_wallet_address, name="submit_wallet_address"),
    path('market-risk/', views.market_risk_view, name='market-risk'),
    path('credit-risk-logistic/', views.credit_risk_logistic_view, name='credit-risk-logistic'),
    path('credit-risk-random-forest/', views.credit_risk_random_forest_view, name='credit-risk-random-forest'),
]

