from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase


class UserAuthTest(TestCase):

    def setUp(self):
        super().setUp()
        self.username = "testuser"
        self.password = "Fat-Chance!"
        self.user1 = User.objects.create_user(
                         username=self.username,
                         password=self.password,
                         email="testuser@nowhere.com")
        self.user1.first_name = "Tester"
        self.user1.save()

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": self.username, "password": self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

    def test_register_view_with_valid_data(self):
        """Test that a user can register as new user with valid data."""
        username = "user-2"
        email = "user@email.com"
        password = "on my way!"
        form_data = {"username": username, "email": email, "password": password}
        response = self.client.post(reverse('polls:register'), form_data)
        user = User.objects.get(username=username)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))

    def test_register_view_with_existed_username(self):
        """Test that a user can't register with existed username"""
        # expect ValueError user already exist
        form_data = {
            "username": self.username,
            "email": "test@g.com",
            "password": self.password
            }
        with self.assertRaises(ValueError):
            _ = self.client.post(reverse('polls:register'), form_data)
