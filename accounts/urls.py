from django.urls import path
from .views import (SignUpView,
                    UserInfoChangeView,
                    UserInfoChangeDoneView,
                    TeamChangeView,
                    TeamChangeDoneView,
                    TeamsEditView)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user_info_change/<int:pk>/", UserInfoChangeView.as_view(), name="user_info_change"),
    path("user_info_change_done/", UserInfoChangeDoneView.as_view(), name="user_info_change_done"),
    path("teams_edit/", TeamsEditView.as_view(), name="teams_edit"),
    path("team_change/<int:pk>/", TeamChangeView.as_view(), name="team_change"),
    path("team_change_done/", TeamChangeDoneView.as_view(), name="team_change_done"),
]
