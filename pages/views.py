import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from vacations.models import Vacation
from accounts.models import Team
from django.contrib.auth import get_user_model


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts'] = self.find_conflicts()
        return context

    @classmethod
    def find_conflicts(cls):
        vacations = Vacation.objects.all()
        teams = Team.objects.all()
        users = get_user_model().objects.all()

        conflicts = list()
        conflicts_info = {}
        for team in teams:
            teammembers = 0
            min_att = float(team.min_attendance) / 100
            for user in users:
                if team == user.team:
                    teammembers += 1
            for vacation in vacations:
                vacation_delta = vacation.end_date - vacation.start_date
                vacation_days = vacation_delta.days
                for processed_delta in range(0, vacation_days + 1):
                    processed_date = vacation.start_date + datetime.timedelta(days=processed_delta)
                    vacationers_on_processed_date = 1
                    for compared_vacation in vacations:
                        vacationers_on_processed_date += cls.get_vacationers(vacation, compared_vacation,
                                                                             processed_date)
                if teammembers > 0 and 1 - (vacationers_on_processed_date / teammembers) < min_att:
                    actual_att = 1 - (vacationers_on_processed_date / teammembers)
                    if processed_date not in conflicts:
                        conflicts.append(processed_date)
                        # conflicts_info[str(processed_date)] = str(user.team)
                        att = {int(actual_att*100): int(min_att*100)}
                        team_att = {str(user.team): att}
                        conflicts_info[processed_date] = team_att
        return conflicts_info

    @classmethod
    def get_vacationers(cls, vacation, compared_vacation, processed_date):
        if not vacation.user == compared_vacation.user:
            user_team = vacation.user.team
            compared_user_team = compared_vacation.user.team
            if user_team == compared_user_team:
                compared_vacation_delta = compared_vacation.end_date - compared_vacation.start_date
                compared_vacation_days = compared_vacation_delta.days
                for compared_processed_delta in range(0, compared_vacation_days + 1):
                    compared_processed_date = compared_vacation.start_date + datetime.timedelta(
                        compared_processed_delta)
                    if processed_date == compared_processed_date:
                        return 1
                    else:
                        return 0
            else:
                return 0
        else:
            return 0
