from django.forms import ModelForm, DateInput
from vacations.models import Vacation


class VacationNewForm(ModelForm):
    class Meta:
        model = Vacation
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}, format='%d.%m.%Y'),
            'end_date': DateInput(attrs={'type': 'date'}, format='%d.%m.%Y'),
        }
        fields = (
            "start_date",
            "end_date",
        )

    def __init__(self, *args, **kwargs):
        super(VacationNewForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        self.fields['end_date'].input_formats = ('%Y-%m-%d',)


class VacationEditForm(ModelForm):
    class Meta:
        model = Vacation
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        fields = (
            "start_date",
            "end_date",
        )

    def __init__(self, *args, **kwargs):
        super(VacationEditForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].input_formats = ('%Y-%m-%d',)
        self.fields['end_date'].input_formats = ('%Y-%m-%d',)
