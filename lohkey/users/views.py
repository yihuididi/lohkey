from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from firestore import db 
from django.shortcuts import render, HttpResponse
from users.wallet_utils import multi_chain_query, analyze_liquidity, fetch_historical_data, fetch_coin_list, analyze_volatility, get_crypto_predictions
from django.http import JsonResponse


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
def wallet_address_view(request):
    if request.method == "POST":
        wallet_address = request.POST.get("wallet_address")

        # Validate wallet address
        if not wallet_address or len(wallet_address) < 5:
            return render(request, "wallet_address.html", {
                "error": "Please provide a valid wallet address."
            })

        # Save wallet address in Firebase and session
        try:
            google_user_id = getattr(request, "google_user_id", None)
            if google_user_id:
                doc_ref = db.collection("walletID").document(google_user_id)
                doc_ref.set({"walletAddress": wallet_address})
                request.session["wallet_address"] = wallet_address
        except Exception as e:
            print(f"Error updating wallet address: {e}")
            return render(request, "wallet_address.html", {
                "error": "An error occurred while saving your wallet address."
            })

        # Redirect to chain selection
        return redirect("select_chains")

    return render(request, "wallet_address.html")

def fetch_token_analysis(request):
    if request.method == "GET":
        token_name = request.GET.get("token_name")
        if not token_name:
            return JsonResponse({"error": "Token name is required."}, status=400)

        # Example: Fetch analysis data for the token
        analysis_data = {
            "liquidity": analyze_liquidity("static/historical_data.json"),  # Replace with token-specific logic
            "volatility": analyze_volatility("static/historical_data.json"),  # Replace with token-specific logic
            "price_prediction": get_crypto_predictions(token_name),  # Replace with actual logic
        }

        return JsonResponse(analysis_data)
    return JsonResponse({"error": "Invalid request method."}, status=405)


def risk_management_view(request):
    return render(request, "risk-management.html")


def risk_advice_view(request):
    return render(request, "risk-advice.html")

def market_risk_view(request):
    if request.method == 'POST':
        stock_ticker = request.POST.get('stock_ticker')
        result = predict_market_risk(stock_ticker)
        return HttpResponse(f"Market Risk Prediction: {result}")
    return render(request, 'market_risk.html')

def credit_risk_logistic_view(request):
    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount'))
        income = float(request.POST.get('income'))
        credit_score = int(request.POST.get('credit_score'))
        debt_to_income_ratio = float(request.POST.get('debt_to_income_ratio'))
        result = predict_credit_risk_logistic(loan_amount, income, credit_score, debt_to_income_ratio)
        return HttpResponse(f"Credit Risk (Logistic Regression): {result}")
    return render(request, 'credit_risk_logistic.html')

def credit_risk_random_forest_view(request):
    if request.method == 'POST':
        loan_amount = float(request.POST.get('loan_amount'))
        income = float(request.POST.get('income'))
        credit_score = int(request.POST.get('credit_score'))
        debt_to_income_ratio = float(request.POST.get('debt_to_income_ratio'))
        result = predict_credit_risk_random_forest(loan_amount, income, credit_score, debt_to_income_ratio)
        return HttpResponse(f"Credit Risk (Random Forest): {result}")
    return render(request, 'credit_risk_random_forest.html')

def select_chains_view(request):
    SUPPORTED_CHAINS = {
    "Ethereum Mainnet": "eth-mainnet",
    "Binance Smart Chain": "bsc-mainnet",
    "Polygon Mainnet": "polygon-mainnet",
    "Avalanche Mainnet": "avalanche-mainnet",
    "Fantom Opera": "fantom-mainnet",
    "Arbitrum One": "arbitrum-mainnet",
    "Optimism": "optimism-mainnet",
    "Solana Mainnet": "solana-mainnet",
    "Moonbeam Mainnet": "moonbeam-mainnet",
    "Harmony Mainnet": "harmony-mainnet",
    "Celo Mainnet": "celo-mainnet",
    "Klaytn Mainnet": "klaytn-mainnet",
    "Cronos Mainnet": "cronos-mainnet",
    "Gnosis Chain": "gnosis-mainnet",
    "Astar Mainnet": "astar-mainnet",
    "Algorand Mainnet": "algorand-mainnet",
    "Near Protocol": "near-mainnet",
    "Tezos Mainnet": "tezos-mainnet",
    "Tron Mainnet": "tron-mainnet",
    "Cardano Mainnet": "cardano-mainnet"
}
    wallet_address = request.session.get("wallet_address")
    if not wallet_address:
        return redirect("wallet_address")

    if request.method == "POST":
        selected_chains = request.POST.getlist("chains")
        if not selected_chains:
            return render(request, "select_chains.html", {
                "error": "Please select at least one blockchain.",
                "chains": SUPPORTED_CHAINS,
            })

        # Save selected chains in session
        request.session["selected_chains"] = selected_chains
        return redirect("portfolio")

    return render(request, "select_chains.html", {"chains": SUPPORTED_CHAINS})

def portfolio_view(request):
    wallet_address = request.session.get("wallet_address")
    selected_chains = request.session.get("selected_chains")

    if not wallet_address or not selected_chains:
        return redirect("wallet_address")

    # Fetch portfolio data
    portfolio = multi_chain_query(wallet_address, selected_chains)
    return render(request, "portfolio.html", {
        "portfolio": portfolio,
        "wallet_address": wallet_address,
    })



def coin_list_view(request):
    """
    Fetches and displays the list of top 50 cryptocurrencies.
    """
    coin_list = fetch_coin_list()
    if "error" in coin_list:
        return render(request, "coin_list.html", {"error": coin_list["error"]})
    return render(request, "coin_list.html", {"coins": coin_list})


def fetch_historical_view(request):
    """
    Fetches historical data for top cryptocurrencies.
    """
    fetch_historical_data()  # Save to static/historical_data.json
    return render(request, "historical_data.html", {"message": "Historical data fetched successfully."})

def liquidity_analysis_view(request):
    """
    Displays liquidity risk analysis for cryptocurrencies.
    """
    json_file = "static/historical_data.json"
    liquidity_data = analyze_liquidity(json_file)
    return render(request, "liquidity_analysis.html", {"liquidity_data": liquidity_data})

def volatility_analysis_view(request):
    """
    Displays volatility risk analysis for cryptocurrencies.
    """
    json_file = "static/historical_data.json"
    volatility_data = analyze_volatility(json_file)
    return render(request, "volatility_analysis.html", {"volatility_data": volatility_data})

def price_prediction_view(request, crypto_symbol):
    """
    Fetches and displays price predictions for a specific cryptocurrency.
    """
    predictions = get_crypto_predictions(crypto_symbol)
    if "error" in predictions:
        return render(request, "price_prediction.html", {"error": predictions["error"]})
    return render(request, "price_prediction.html", {"predictions": predictions})
