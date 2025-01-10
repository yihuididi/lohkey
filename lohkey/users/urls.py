from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    # Home Page
    path("", views.home, name="home"),
    
    # User Authentication
    path('accounts/login/', lambda request: redirect('socialaccount_login', provider='google'), name="login"),
    path("logout", views.logout_view, name="logout"),
    
    # Portfolio Views
    path("wallet-address/", views.wallet_address_view, name="wallet_address"),
    path("select-chains/", views.select_chains_view, name="select_chains"),
    path("portfolio/", views.portfolio_view, name="portfolio"),
    
    # Risk Management and Advice
    path("risk-management/", views.risk_management_view, name="risk_management"),
    path("risk-advice/", views.risk_advice_view, name="risk_advice"),
    
    # Market Risk Views
    path('market-risk/', views.market_risk_view, name='market_risk'),
    path('credit-risk-logistic/', views.credit_risk_logistic_view, name='credit_risk_logistic'),
    path('credit-risk-random-forest/', views.credit_risk_random_forest_view, name='credit_risk_random_forest'),
    
    # Additional Features
    path("coins/", views.coin_list_view, name="coin_list"),
    path("historical/", views.fetch_historical_view, name="fetch_historical"),
    path("liquidity/", views.liquidity_analysis_view, name="liquidity_analysis"),
    path("volatility/", views.volatility_analysis_view, name="volatility_analysis"),
    path("predictions/<str:crypto_symbol>/", views.price_prediction_view, name="price_prediction"),
]

