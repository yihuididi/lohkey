from django.urls import path
from . import views

urlpatterns = [
    path("", views.home),
    path("logout", views.logout_view),
    path("portfolio", views.portfolio_view),
    path("risk-management", views.risk_management_view),
    path("risk-advice", views.risk_advice_view)
]