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
        context['conflicts_team'] = self.find_conflicts_team()
        context['conflicts_division'] = self.find_conflicts_division()
        context['conflicts_department'] = self.find_conflicts_department()
        return context

    def find_conflicts_department(self):
        # get all divisions of the user's department
        divisions = Division.objects.filter(department=self.request.user.team.division.department)

        # get all conflicts of all divisions in the user's department
        conflicts = list()
        for division in divisions:
            conflicts.append(self.find_conflicts_division(division))

        return conflicts

    def find_conflicts_division(self, division=None):
        # get all teams of the user's division
        if division is None:
            teams = Team.objects.filter(division=self.request.user.team.division)
            for team in teams:
                json_conflicts = json.loads(self.find_conflicts_team(team))
                print(json_conflicts)
        else:
            teams = Team.objects.filter(division=division)

        # get all conflicts of all teams in the user's division
        conflicts = list()
        for team in teams:
            if self.find_conflicts_team(team) and not self.find_conflicts_team(team) == "[]":
                conflicts.append(self.find_conflicts_team(team))

        return conflicts

    def find_conflicts_team(self, team=None):
        user = self.request.user
        vacations = Vacation.objects.all()
        users = get_user_model().objects.all()

        if team is None:
            team = user.team
        else:
            team = team

        conflict_dates_helper = list()
        conflict_dates_list = list()

        # get count of user's team members
        team_members = users.filter(team=team)
        team_members_count = team_members.count()

        min_att = float(team.min_attendance) / 100

        # filter all vacations of the user's team
        vacations = vacations.filter(user__team=team)

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
                        conflicts_list = {"date": str(processed_date),
                                          "team": str(team),
                                          "att": actual_att * 100,
                                          "min_att": min_att * 100}
                        conflict_dates_list.append(conflicts_list)
        conflict_dates_json = json.loads(json.dumps(conflict_dates_list))
        sorted_conflict_dates_json = sorted(conflict_dates_json, key=lambda k: k['date'])

        return json.dumps(sorted_conflict_dates_json)
