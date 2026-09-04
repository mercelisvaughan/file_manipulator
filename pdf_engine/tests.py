from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class GuestRateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        # If your middleware checks request.path == '/upload/',
        # make sure this targets that exact URL or reverse name
        self.upload_url = '/upload/'

    def test_guest_upload_limit_enforced_after_three_attempts(self):
        """Guests should be permitted up to 3 actions before forced redirect."""
        session = self.client.session
        session['guest_usage_count'] = 4
        session.save()

        # A guest with count >= 3 should be redirected away from the upload tool
        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('register'), response.url)

    def test_authenticated_user_bypasses_guest_limit(self):
        """Authenticated users must not be blocked by guest session counts."""
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        session = self.client.session
        session['guest_usage_count'] = 5
        session.save()

        response = self.client.get(self.upload_url)
        # Should successfully load the page instead of redirecting
        self.assertEqual(response.status_code, 200)