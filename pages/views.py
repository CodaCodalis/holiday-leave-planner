import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from vacations.models import Vacation
from accounts.models import Division, Team, Employee
from django.contrib.auth import get_user_model
import json


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts_team'] = json.dumps(self.find_conflicts_team())
        context['conflicts_division'] = self.find_conflicts_division()
        context['conflicts_department'] = self.find_conflicts_department()
        return context

    def find_conflicts_department(self):
        # get all divisions of the user's department
        divisions = Division.objects.filter(department=self.request.user.team.division.department)

        # get all conflicts of all divisions in the user's department
        conflicts_by_division = list()
        for division in divisions:
            conflicts_by_division.append(self.find_conflicts_division(division))

        # get all teams with conflicts
        conflicts_department = list()
        for conflicts in conflicts_by_division:
            divisions = list()
            teams = list()
            division = None
            for conflict in conflicts:
                teams.append(conflict[0])
                division = self.request.user.team.division

            if division is not None:
                divisions.append(division)
                divisions.append(teams)

            if divisions:
                conflicts_department.append(divisions)

        print(conflicts_department)

        return conflicts_department

    def find_conflicts_division(self, division=None):
        # get all teams of the user's division
        if division is None:
            teams = Team.objects.filter(division=self.request.user.team.division)
        else:
            teams = Team.objects.filter(division=division)

        # get all conflicts of all teams in the user's division
        conflicts_by_team = list()
        for team in teams:
            conflicts_by_team.append(self.find_conflicts_team(team))

        conflicts_divison = list()
        for conflicts in conflicts_by_team:
            teams = list()
            dates = list()
            team = None
            for conflict in conflicts:
                dates.append(datetime.datetime.strptime(conflict['date'], '%Y-%m-%d'))
                team = conflict['team']

            if team is not None:
                teams.append(team)
                teams.append(dates)

            if teams:
                conflicts_divison.append(teams)

        return conflicts_divison

    def find_conflicts_team(self, team=None):
        if team is None:
            user = self.request.user
            team = user.team

        # get all vacations and users
        vacations = Vacation.objects.all()
        users = get_user_model().objects.all()

        # filter all vacations and users of the user's team
        vacations = vacations.filter(user__team=team)
        users = users.filter(team=team)

        # get count of user's team members
        team_members_count = users.count()

        # min attendance of processed team
        min_att = float(team.min_attendance) / 100

        # find conflicts
        conflict_dates_helper = list()
        conflicts = list()

        for vacation in vacations:
            vacation_delta = vacation.end_date - vacation.start_date
            vacation_days = vacation_delta.days
            for processed_delta in range(0, vacation_days + 1):
                processed_date = vacation.start_date + datetime.timedelta(days=processed_delta)
                vacationers_on_processed_date = 1
                for compared_vacation in vacations:
                    if not vacation.user == compared_vacation.user:
                        compared_vacation_delta = compared_vacation.end_date - compared_vacation.start_date
                        compared_vacation_days = compared_vacation_delta.days
                        for compared_processed_delta in range(0, compared_vacation_days + 1):
                            compared_processed_date = compared_vacation.start_date + datetime.timedelta(
                                days=compared_processed_delta)
                            if processed_date == compared_processed_date:
                                vacationers_on_processed_date += 1
                if team_members_count > 0 and 1 - (vacationers_on_processed_date / team_members_count) < min_att:
                    actual_att = 1 - (vacationers_on_processed_date / team_members_count)
                    if processed_date not in conflict_dates_helper:
                        conflict_dates_helper.append(processed_date)
                        conflict = {"date": str(processed_date),
                                    "team": str(team),
                                    "att": actual_att * 100,
                                    "min_att": min_att * 100}
                        conflicts.append(conflict)
        sorted_conflicts = sorted(conflicts, key=lambda k: k['date'])

        return sorted_conflicts
