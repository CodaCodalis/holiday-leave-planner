from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee, Team


class EmployeeCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Employee
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "reg_num",
            "supervisor",
            "team",
            "role",
        )


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "reg_num",
            "supervisor",
            "team",
            "role",
        )


class TeamCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Team
        fields = (
            "name",
            "head",
            "min_attendance",
            "division",
        )


class TeamChangeForm(UserChangeForm):
    class Meta:
        model = Team
        fields = (
            "name",
            "head",
            "min_attendance",
            "division",
        )
