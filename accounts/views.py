from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EmployeeCreationForm


class SignUpView(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
