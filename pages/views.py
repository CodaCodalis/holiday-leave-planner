import datetime

from django.views.generic import TemplateView
from vacations.models import Vacation
from accounts.models import Team
from django.contrib.auth import get_user_model


class HomePageView(TemplateView):
    template_name = "home.html"
    vacations = Vacation.objects.all()
    teams = Team.objects.all()
    User = get_user_model()
    users = User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # current_user = self.request.user
        context['dates_with_conflict'] = self.find_conflicts(self.teams, self.users, self.vacations)
        # context['current_user'] = current_user
        return context

    @classmethod
    def find_conflicts(cls, teams, users, vacations):
        dates_with_conflict = list()
        # für jedes team die anzahl der teammitglieder ermitteln
        for team in teams:
            teammembers = 0
            min_att = team.min_attendance
            for user in users:
                if team == user.team:
                    teammembers += 1
            # für jeden urlaubseintrag die anzahl der mitglieder ermitteln, die am gleichen tag urlaub genommen haben
            vacationers_on_processed_date = 0
            for vacation in vacations:
                # anzahl der urlaubstage des betrachteten urlaubseintrags ermitteln
                vacation_delta = vacation.end_date - vacation.start_date
                vacation_days = vacation_delta.days
                for processed_delta in range(0, vacation_days+1):
                    processed_date = vacation.start_date + datetime.timedelta(processed_delta)
                    # den verarbeiteten tag in den urlaubsanträgen anderer teammitglieder suchen
                    for compared_vacation in vacations:
                        if not vacation.user == compared_vacation.user:
                            compared_vacation_delta = compared_vacation.end_date - compared_vacation.start_date
                            compared_vacation_days = compared_vacation_delta.days
                            for compared_processed_delta in range(0, compared_vacation_days+1):
                                compared_processed_date = vacation.start_date + datetime.timedelta(compared_processed_delta)
                                if processed_date == compared_processed_date:
                                    vacationers_on_processed_date += 1
                    if vacationers_on_processed_date > 0 and teammembers > 0 and 1 - (vacationers_on_processed_date / teammembers) < float(min_att) / 100:
                        dates_with_conflict.append(processed_date)

        return dates_with_conflict
