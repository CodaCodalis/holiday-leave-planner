from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .models import Employee

from .forms import EmployeeCreationForm, EmployeeChangeForm


class SignUpView(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserInfoView(UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('home')
    template_name = "registration/user_info.html"

