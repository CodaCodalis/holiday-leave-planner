from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Employee


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
        )
