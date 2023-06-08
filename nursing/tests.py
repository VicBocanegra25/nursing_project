from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.http import HttpResponse

# Importing our first class-based view
from .views import HomePageView
from .forms import SubmitDataForm


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


# Testing the form for submitting data
class SubmitDataFormTest(TestCase):
    def setUp(self):
        # The Django test client emulates a web browser in code, letting us simulate GET and POST requests to our views and check the responses.
        self.client = Client()

    def test_submit_page_url(self):
        # Test that the URL for the submit view resolves correctly
        response = self.client.get("/submit/")
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        # Tests that the form is valid when given correct data.
        form_data = {
            "name": "Test Name",
            "last_name": "Test Last Name",
            "age": 30,
            "email": "test@example.com",
        }
        form = SubmitDataForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        # Tests that the form is invalid when the email is not in the correct format.
        form_data = {
            "name": "Test Name2",
            "last_name": "Test Last Name*",
            "age": 30,
            "email": "invalid email",
        }
        form = SubmitDataForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_submit_page_uses_correct_template(self):
        # Tests that the correct template is used for the form page.
        response = self.client.get(reverse("submit"))
        self.assertTemplateUsed(response, "submit_data.html")
