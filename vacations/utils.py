from datetime import date
from calendar import HTMLCalendar
from .models import Vacation
from accounts.models import CustomUser
from django.contrib.auth import get_user_model


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, vacations, user, teammember_count):
        d = ''
        color = f'style="background-color:#cccccc;"'
        dot_color = '#43C532'
        min_att = 0.5
        if day != 0:
            processed_date = date(self.year, self.month, day)
            vacationers = 0
            for vacation in vacations:
                if vacation.is_on_date(processed_date) and user.team == vacation.user.team:
                    d += f'<li> {vacation.get_html_url} </li>'
                    vacationers += 1
            if vacationers > 0 and vacationers/teammember_count >= min_att:
                dot_color = '#F6D200'
            if vacationers > 0 and vacationers / teammember_count < min_att:
                dot_color = '#D10A11'

            return f"<td {color}><span>{day}</span><font color='{dot_color}'> &#11044; </font><ul style='list-style-type:none'> {d} </ul></td>"
        return f'<td {color}></td>'

    def formatweek(self, theweek, vacations, user, teammember_count):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, vacations, user, teammember_count)
        return f'<tr> {week} </tr>'

    def formatmonth(self, user, withyear=True):
        vacations = Vacation.objects.all()
        teammember_count = self.count_teammembers(user)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, vacations, user, teammember_count)}\n'
        return cal

    def count_teammembers(self, logged_in_user):
        User = get_user_model()
        users = User.objects.all()
        counter = 0
        for user in users:
            if user.team == logged_in_user.team:
                counter += 1
        return counter
