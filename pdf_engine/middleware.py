from django.shortcuts import redirect
from django.contrib import messages

class GuestSessionRateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. Bypass completely for logged-in users
        if request.user.is_authenticated:
            return self.get_response(request)

        # 2. Check if they are interacting with the upload page (GET or POST)
        if request.path == '/upload/':
            
            # Fetch current count
            usage_count = request.session.get('guest_usage_count', 0)

            # 3. IMMEDIATELY redirect if they are at the limit (Even on page load/GET)
            if usage_count >= 3:
                messages.warning(request, "You've reached your free daily limit! Create an account to continue.")
                return redirect('register')

            # 4. ONLY increment the counter if they are actually uploading (POST)
            if request.method == 'POST':
                request.session['guest_usage_count'] = usage_count + 1

        # Continue processing the request normally
        return self.get_response(request)