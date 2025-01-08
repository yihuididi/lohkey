from allauth.socialaccount.models import SocialAccount

class GoogleUserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            social_account = SocialAccount.objects.filter(user=request.user, provider="google").first()
            if social_account:
                request.google_user_id = social_account.uid
                print(f"Google User ID found: {request.google_user_id}")
            else:
                request.google_user_id = None
                print("No linked Google account.")
        else:
            request.google_user_id = None
            print("User is not authenticated.")
        response = self.get_response(request)
        return response