from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from .models import Employee

from .forms import EmployeeCreationForm, EmployeeChangeForm


class SignUpView(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserInfoChangeView(UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('user_info_change_done')
    template_name = "registration/user_info_change_form.html"


class UserInfoChangeDoneView(TemplateView):
    template_name = "registration/user_info_change_done.html"
