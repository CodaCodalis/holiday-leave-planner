from django.urls import path

from .views import (CalendarView,
                    VacationDetailView,
                    VacationDeleteView,
                    VacationCreateView,
                    VacationUpdateView,
                    VacationsOverviewView)

urlpatterns = [
    path("", CalendarView.as_view(), name="calendar"),
    path("new/", VacationCreateView.as_view(), name='vacation_new'),
    path("<int:pk>/", VacationDetailView.as_view(), name='vacation_detail'),
    path("edit/<int:pk>/", VacationUpdateView.as_view(), name='vacation_edit'),
    path("delete/<int:pk>", VacationDeleteView.as_view(), name='vacation_delete'),
    path("overview/", VacationsOverviewView.as_view(), name='vacations_overview'),
]
