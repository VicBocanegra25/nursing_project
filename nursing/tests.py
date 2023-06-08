from django.test import TestCase
from django.urls import reverse, resolve
from django.http import HttpResponse

# Importing our first class-based view
from .views import HomePageView


class HomePageTests(TestCase):
    # We're making a GET request to the homepage, and saving the response to use in our tests.
    def setUp(self):
        self.response = self.client.get("/")

    def test_homepage_status_code(self):
        # Testing that the homepage returns a 200 status code
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_url_name(self):
        # Testing that the url name for the homepage resolves correctly
        self.assertEqual(resolve("/").func.view_class, HomePageView)

    def test_homepage_template(self):
        # Testing that the correct template is used for the homepage
        self.assertTemplateUsed(self.response, "home.html")
