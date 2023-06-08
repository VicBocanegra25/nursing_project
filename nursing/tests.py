from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.http import HttpResponse
from django.contrib import messages as messages_module
from .models import UserApplication

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


# Creating test cases to make sure that the form is creating objects and storing them in the database.
class UserApplicationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_application(self):
        # Getting the current count of UserApplication objects
        initial_count = UserApplication.objects.count()

        # Simulate form submission
        response = self.client.post(
            reverse("submit"),
            {
                "name": "Jon",
                "last_name": "Snow",
                "age": "30",
                "email": "jon.snow@got.com",
            },
            follow=True,
        )

        # Check that the form submission was successful(must redirect to homepage)
        self.assertEqual(response.status_code, 200)

        # Check that the new UserApplication object was created
        new_count = UserApplication.objects.count()
        self.assertEqual(new_count, initial_count + 1)

        # Check that the new UserApplication has the correct data
        new_application = UserApplication.objects.latest("id")
        self.assertEqual(new_application.name, "Jon")
        self.assertEqual(new_application.last_name, "Snow")
        self.assertEqual(new_application.age, 30)
        self.assertEqual(new_application.email, "jon.snow@got.com")

        # Test for a success message after submission
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        message = messages[0]
        self.assertEqual(message.level, messages_module.SUCCESS)
        self.assertEqual(
            message.message, "Your form was submitted successfully. Danke!"
        )
