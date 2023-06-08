# Creating a class-based view for a simple homepage
from django.views import View
from django.shortcuts import render, redirect
from .models import UserApplication
from .forms import SubmitDataForm
from django.contrib import messages

from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from .forms import SubmitDataForm


class HomePageView(TemplateView):
    # This is a simple class-based view that will render the home.html template
    template_name = "home.html"


class SubmitDataView(FormView):
    # Now we're actually using a Form View to collect data
    template_name = "submit_data.html"
    form_class = SubmitDataForm
    # Redirect to the homepage after submitting the form
    success_url = "/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        UserApplication.objects.create(
            name=form.cleaned_data["name"],
            last_name=form.cleaned_data["last_name"],
            age=form.cleaned_data["age"],
            email=form.cleaned_data["email"],
        )
        messages.success(self.request, "Your form was submitted successfully. Danke!")
        return super().form_valid(form)
