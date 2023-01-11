from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

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


class EmployeeChangeForm(forms.ModelForm):
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


class TeamCreationForm(forms.ModelForm):
    class Meta(forms.ModelForm):
        model = Team
        fields = (
            "name",
            "head",
            "min_attendance",
            "division",
        )


class TeamChangeForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = (
            "name",
            "head",
            "min_attendance",
            "division",
        )
