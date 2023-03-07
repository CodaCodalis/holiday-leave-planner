from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Employee, Team, Division


class EmployeeCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    reg_num = forms.CharField(initial=123456, required=False)
    supervisor = forms.ModelChoiceField(queryset=Employee.objects.filter(role='HODiv'), required=True)
    division = forms.ModelChoiceField(queryset=Division.objects.all())
    team = forms.ModelChoiceField(queryset=Team.objects.none(), disabled=True)
    role = forms.ChoiceField(initial='Emp', disabled=True, choices=Employee.Role.choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team'].queryset = Team.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['team'].queryset = Team.objects.filter(division_id=division_id).order_by('name')
                self.fields['team'].disabled = False
            except (ValueError, TypeError):
                pass

    class Meta(UserCreationForm):
        model = Employee
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "reg_num",
            "supervisor",
            "division",
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
        )
