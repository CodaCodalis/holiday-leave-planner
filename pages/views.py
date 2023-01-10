from django.views.generic import TemplateView
from vacations.models import Vacation


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacations'] = Vacation.objects.all()
        return context
