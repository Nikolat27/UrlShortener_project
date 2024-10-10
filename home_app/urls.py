from . import views
from django.urls import path

app_name = "home_app"
urlpatterns = [
    path("", views.home_page, name="main_page"),
    path("generator", views.random_generator, name="random_generator"),
]
