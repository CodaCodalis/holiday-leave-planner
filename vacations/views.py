from datetime import date, timedelta
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from django.utils.safestring import mark_safe
import calendar

from .utils import Calendar
from .models import *


class CalendarView(ListView):
    model = Vacation
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request.user, withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = self.prev_month(d)
        context['next_month'] = self.next_month(d)
        return context

    @classmethod
    def get_date(cls, req_day):
        if req_day:
            year, month = (int(x) for x in req_day.split('-'))
            return date(year, month, day=1)
        return date.today()

    @classmethod
    def prev_month(cls, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    @classmethod
    def next_month(cls, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month


class VacationCreateView(CreateView):
    model = Vacation
    template_name = "vacation_new.html"
    fields = (
        "start_date",
        "end_date",
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class VacationDetailView(DetailView):
    model = Vacation
    template_name = "vacation_detail.html"


class VacationDeleteView(DeleteView):
    model = Vacation
    template_name = "vacation_delete.html"
    success_url = reverse_lazy("calendar")


class VacationUpdateView(UpdateView):
    model = Vacation
    fields = (
        "start_date",
        "end_date",
    )
    template_name = "vacation_edit.html"
