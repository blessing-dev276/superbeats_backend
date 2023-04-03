from . import views
from django.urls import path, include

urlpatterns = [
    path("api/signin/", views.SigninAPI.as_view(), name="signin"),
    path("api/refresh/", views.RefreshAPI.as_view(), name="refresh"),
    # path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("api/signup/", views.SignupAPI.as_view({"post": "create"}), name="signup"),
]
