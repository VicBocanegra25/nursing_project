# Creating a class-based view for a simple homepage
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    # This is a simple class-based view that will render the home.html template
    template_name = "home.html"
