from django.urls import path
from .views import HomePageView
from . import views

urlpatterns = [
    # The path function is mapping "" to our HomePageView.
    path("", HomePageView.as_view(), name="home"),
    # Adding our submit data view
    path("submit/", views.SubmitDataView.as_view(), name="submit"),
]
