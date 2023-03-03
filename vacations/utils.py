from datetime import date
from calendar import LocaleHTMLCalendar
from .models import Vacation
from django.contrib.auth import get_user_model


class Calendar(LocaleHTMLCalendar):
    def __init__(self, year=None, month=None, locale='de_DE'):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, vacations, user):
        d = ''

        if day != 0:
            processed_date = date(self.year, self.month, day)
            vacationers_in_team = 0
            for vacation in vacations:
                if vacation.is_on_date(processed_date) and user.team == vacation.user.team and user == vacation.user:
                    d += f'<li><a class="dropdown-item" href="{vacation.get_html_url}"><u>{vacation.user.first_name} {vacation.user.last_name}</u></a></li>'
                    vacationers_in_team += 1
                elif vacation.is_on_date(processed_date) and user.team == vacation.user.team:
                    d += f'<li><a class="dropdown-item" href="#">{vacation.user.first_name} {vacation.user.last_name}</a></li>'
                    vacationers_in_team += 1
            td_class = self.get_td_class(user, vacationers_in_team)
            teammembers = self.count_teammembers(user)
            if vacationers_in_team > 0:
                return f'<td class="{td_class}"><span>{day}</span><div class="dropdown"><button class="btn btn-outline-secondary ' \
                       f'dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown" ' \
                       f'aria-expanded="false">{vacationers_in_team}/{teammembers}</button><ul class="dropdown-menu" ' \
                       f'aria-labelledby="dropdownMenuButton1"> {d} </ul></div></td> '
            else:
                return f'<td class="{td_class}"><span>{day}</span></td> '
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

    def get_td_class(self, user, vacationers):
        min_att = float(user.team.min_attendance) / 100.0
        teammembers = self.count_teammembers(user)
        td_class = 'conflict-free'  # green
        if vacationers > 0 and 1 - (vacationers / teammembers) >= min_att:
            td_class = 'warning'  # yellow
        if vacationers > 0 and 1 - (vacationers / teammembers) < min_att:
            td_class = 'conflict'  # red
        return td_class
