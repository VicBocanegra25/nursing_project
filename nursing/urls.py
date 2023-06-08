from django.urls import path
from .views import HomePageView

urlpatterns = [
    # The path function is mapping "" to our HomePageView.
    path("", HomePageView.as_view(), name="home"),
]
