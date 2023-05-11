import datetime
import math

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from vacations.models import Vacation
from accounts.models import Division, Team, Employee
import json


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['conflicts_team'] = json.dumps(self.reveal_conflicts_in_team_and_return_list())
        context['conflicts_division'] = self.collect_conflicts_in_division_and_return_list()
        context['conflicts_department'] = self.collect_conflicts_in_department_and_return_list()
        return context

    def collect_conflicts_in_department_and_return_list(self):
        # get all divisions of the user's department
        divisions = self.get_all_divisions_of_department()

        # get all conflicts of all divisions in the user's department
        conflicts_in_divisions = self.get_list_of_conflicts_in_divisions(divisions)

        # get all teams with conflicts
        conflicts_department = list()
        for conflicts in conflicts_in_divisions:
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

        return conflicts_department

    def get_all_divisions_of_department(self):
        return Division.objects.filter(department=self.request.user.team.division.department)
    def get_list_of_conflicts_in_divisions(self, divisions):
        conflicts_in_divisions = list()
        for division in divisions:
            conflicts_in_divisions.append(self.collect_conflicts_in_division_and_return_list(division))
        return conflicts_in_divisions
    def collect_conflicts_in_division_and_return_list(self, division=None):
        # get all teams of the user's division
        if division is None:
            teams = Team.objects.filter(division=self.request.user.team.division)
        else:
            teams = Team.objects.filter(division=division)

        # get all conflicts of all teams in the user's division
        conflicts_by_team = list()
        for team in teams:
            conflicts_by_team.append(self.reveal_conflicts_in_team_and_return_list(team))

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

    def reveal_conflicts_in_team_and_return_list(self, team=None):
        if team is None:
            team = self.request.user.team

        team_vacation_objects = self.get_vacation_objects_of_team(team)
        team_members_count = self.get_number_of_employee_objects_in_team(team)
        team_min_att = self.get_min_attendance_of_team(team)
        team_vacation_dates = self.get_vacation_dates(team_vacation_objects)
        team_conflicts_list = self.create_conflicts_list(team_vacation_dates, team_min_att, team_members_count, team)

        return team_conflicts_list

    def get_vacation_objects_of_team(self, team):
        return Vacation.objects.all().filter(user__team=team)

    def get_number_of_employee_objects_in_team(self, team):
        return Employee.objects.all().filter(team=team).count()

    def get_min_attendance_of_team(self, team):
        return float(team.min_attendance) / 100

    def get_vacation_dates(self, vacations):
        vacation_dates = list()
        for vacation in vacations:
            vacation_length = self.get_vacation_length(vacation)
            for processed_delta in range(0, vacation_length + 1):
                vacation_date = vacation.start_date + datetime.timedelta(days=processed_delta)
                vacation_dates.append(vacation_date)
        return vacation_dates

    def get_vacation_length(self, vacation):
        return (vacation.end_date - vacation.start_date).days

    def create_conflicts_list(self, vacation_dates, min_att, num_team_members, team):
        vacation_dates_occurrences_dict = self.get_num_of_occurences_of_dates(vacation_dates)
        num_required_employees = self.compute_num_required_employees(num_team_members, team.min_attendance)
        conflicts_list = list()
        for occurrence in vacation_dates_occurrences_dict:
            if vacation_dates_occurrences_dict[occurrence] > (num_team_members - num_required_employees):
                conflict_dict = {"date": str(occurrence),
                                 "team": str(team),
                                 "att": round(vacation_dates_occurrences_dict[occurrence] / num_team_members * 100, 1),
                                 "min_att": min_att * 100}
                conflicts_list.append(conflict_dict)
        return conflicts_list

    def get_num_of_occurences_of_dates(self, vacation_dates):
        return {i: vacation_dates.count(i) for i in vacation_dates}

    def compute_num_required_employees(self, num_team_members, min_attendance):
        return math.ceil(num_team_members * float(min_attendance) / 100)
