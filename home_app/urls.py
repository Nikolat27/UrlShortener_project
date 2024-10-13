from . import views
from django.urls import path

app_name = "home_app"
urlpatterns = [
    path("", views.home_page, name="main_page"),
    path("login", views.LoginPageView.as_view(), name="login_page"),
    path("<str:shorted_url>", views.redirect_view, name="redirect_view"),
    path("validate-password/<str:shorted_url>/", views.validate_password, name="validate_password"),
    path("pendingApproval_requests/", views.pendingApproval_requests, name="pendingApproval_requests"),
    path("approve/<int:pk>/", views.approve_request, name="approve_request"),
    path("reject/<int:pk>/", views.reject_request, name="reject_request"),
    path("create/", views.create, name="create"),
    path("update/<str:shorted_url>/", views.update_url, name="update_url"),
    path("delete/<str:shorted_url>/", views.delete_url, name="delete_url"),
    path("get_url_details/<str:shorted_url>/", views.get_url_details, name="get_url_details"),
    path('get_urls/', views.get_user_urls, name='get_user_urls'),  # New endpoint for retrieving user's URLs
]
