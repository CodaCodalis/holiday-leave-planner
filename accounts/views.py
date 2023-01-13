from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from .models import Employee, Team
from .forms import EmployeeCreationForm, EmployeeChangeForm, TeamChangeForm


class SignUpView(LoginRequiredMixin, CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class UserInfoChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Employee
    form_class = EmployeeChangeForm
    success_url = reverse_lazy('user_info_change_done')
    template_name = "registration/user_info_change_form.html"

    def test_func(self):
        obj = self.get_object()
        return obj.id == self.request.user.id


class UserInfoChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "registration/user_info_change_done.html"


class TeamChangeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    form_class = TeamChangeForm
    success_url = reverse_lazy('team_change_done')
    template_name = "registration/team_change_form.html"

    def test_func(self):
        obj = self.get_object()
        return obj.head.team.division.head == self.request.user


class TeamChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "registration/team_change_done.html"


class TeamsEditView(LoginRequiredMixin, TemplateView):
    template_name = "registration/teams_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.all()
        return context
