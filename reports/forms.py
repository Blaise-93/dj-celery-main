from django import forms
from .models import Report


class ReportModelForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = [
            'name',
            'remarks',

        ]
