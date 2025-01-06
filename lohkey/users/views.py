from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from firestore import db 

@login_required
def home(request):

    return render(request, "home.html", {"google_user_id": request.google_user_id})

def logout_view(request):
    logout(request)
    return redirect("/")

@login_required
def portfolio_view(request):
    try:
        print(f"Inside portfolio_view. Google User ID: {request.google_user_id}")

        if not request.google_user_id:
            print("Google User ID is missing.")
            return render(request, "portfolio.html", {"error": "Google account is not linked."})

        # Check if walletID exists in Firebase
        doc_ref = db.collection("walletID").document(request.google_user_id)
        wallet_data = doc_ref.get()

        if wallet_data.exists:
            wallet_address = wallet_data.to_dict().get("walletAddress")
            print(f"Wallet Address found: {wallet_address}")
        else:
            wallet_address = None
            print("No Wallet Address found.")

        return render(request, "portfolio.html", {"wallet_address": wallet_address})
    except Exception as e:
        print(f"Error in portfolio_view: {e}")
        return render(request, "portfolio.html", {"error": "An error occurred while loading the portfolio page."})

@login_required
def submit_wallet_address(request):
    if request.method == "POST":
        # Retrieve wallet address from the form
        wallet_address = request.POST.get("wallet_address")
        
        # Save or update the wallet address in Firebase
        try:
            if request.google_user_id:
                doc_ref = db.collection("walletID").document(request.google_user_id)
                doc_ref.set({"walletAddress": wallet_address})
                print(f"Wallet Address updated: {wallet_address}")
            else:
                print("Google User ID is missing.")
        except Exception as e:
            print(f"Error updating wallet address: {e}")
        
        # Redirect to the portfolio page
        return redirect("/portfolio")

    return render(request, "portfolio.html")


def risk_management_view(request):
    return render(request, "risk-management.html")


def risk_advice_view(request):
    return render(request, "risk-advice.html")

 
