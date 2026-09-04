from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class GuestRateLimitMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = '/upload/'

    def test_guest_upload_limit_enforced_after_three_attempts(self):
        """Guests should be redirected after reaching the 3-upload limit."""
        session = self.client.session
        session['guest_usage_count'] = 3
        session.save()

        response = self.client.get(self.upload_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('register'), response.url)

    def test_authenticated_user_bypasses_guest_limit(self):
        """Authenticated users must not be blocked by guest session counts."""
        User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        session = self.client.session
        session['guest_usage_count'] = 5
        session.save()

        response = self.client.get(self.upload_url)
        self.assertNotEqual(response.status_code, 302)