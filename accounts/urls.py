from django.urls import path
from .views import SignUpView, UserInfoView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user_info/<int:pk>/", UserInfoView.as_view(), name="user_info"),
]
