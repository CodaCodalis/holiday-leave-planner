from datetime import date
from calendar import HTMLCalendar
from .models import Vacation
from django.contrib.auth import get_user_model


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, vacations, user):
        d = ''

        if day != 0:
            processed_date = date(self.year, self.month, day)
            vacationers_in_team = 0
            for vacation in vacations:
                if vacation.is_on_date(processed_date) and user.team == vacation.user.team:
                    d += f'<li> {vacation.get_html_url} </li>'
                    vacationers_in_team += 1
            dot = self.get_dot(user, vacationers_in_team)
            td_class = self.get_td_class(user, vacationers_in_team)
            return f'<td class="{td_class}"><span>{day}</span><ul style="list-style-type:none"> {d} </ul></td>'
        return f'<td></td>'

    def formatweek(self, theweek, vacations, user):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, vacations, user)
        return f'<tr> {week} </tr>'

    def formatmonth(self, user, withyear=True):
        vacations = Vacation.objects.all()
        cal = f'<table class="calendar table-primary">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, vacations, user)}\n'
        return cal

    def count_teammembers(self, logged_in_user):
        User = get_user_model()
        users = User.objects.all()
        teammembers = 0
        for user in users:
            if user.team == logged_in_user.team:
                teammembers += 1
        return teammembers

    def get_dot(self, user, vacationers):
        min_att = float(user.team.min_attendance) / 100.0
        # min_att = 0.33
        teammembers = self.count_teammembers(user)
        dot_color = '#43C532'  # green
        if vacationers > 0 and 1 - (vacationers / teammembers) >= min_att:
            dot_color = '#F6D200'  # yellow
        if vacationers > 0 and 1 - (vacationers / teammembers) < min_att:
            dot_color = '#D10A11'  # red
        return f'<font color="{dot_color}"> &#11044; </font>'

    def get_td_class(self, user, vacationers):
        min_att = float(user.team.min_attendance) / 100.0
        teammembers = self.count_teammembers(user)
        td_class = 'conflict-free'  # green
        if vacationers > 0 and 1 - (vacationers / teammembers) >= min_att:
            td_class = 'warning'  # yellow
        if vacationers > 0 and 1 - (vacationers / teammembers) < min_att:
            td_class = 'conflict'  # red
        return td_class
