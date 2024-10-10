from . import views
from django.urls import path

app_name = "home_app"
urlpatterns = [
    path("", views.home_page, name="main_page"),
    path("create/", views.create, name="create"),
    path("update/<str:shorted_url>", views.update_url, name="update_url"),
    path("delete/<str:shorted_url>", views.delete_url, name="delete_url"),
    path('get_urls/', views.get_user_urls, name='get_user_urls'),  # New endpoint for retrieving user's URLs
]
