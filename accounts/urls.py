from django.urls import path
from .views import SignUpView, UserInfoChangeView, UserInfoChangeDoneView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user_info_change/<int:pk>/", UserInfoChangeView.as_view(), name="user_info_change"),
    path("user_info_change_done/", UserInfoChangeDoneView.as_view(), name="user_info_change_done"),
]
