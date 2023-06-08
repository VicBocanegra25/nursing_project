# Creating a class-based view for a simple homepage
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
