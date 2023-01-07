from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils import timezone


class Vacation(models.Model):
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user) + ": " + str(self.start_date) + " - " + str(self.end_date)

    def get_absolute_url(self):
        return reverse("vacation_detail", kwargs={"pk": self.pk})

    @property
    def get_html_url(self):
        url = reverse('vacation_detail', args=(self.pk,))
        return f'<a href="{url}"> {self.user.first_name} {self.user.last_name} </a>'

    def is_on_date(self, processed_date):
        if self.start_date <= processed_date <= self.end_date and processed_date.weekday() < 5:
            return True
        else:
            return False
