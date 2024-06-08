from django import forms


class SalesSearchForm(forms.Form):

    CHART_CHOICES = (
        ("#1", "Bar chart"),
        ("#2", "Pie chart"),
        ("#3", "Line chart"),
    )

    RESULT_CHOICES =  (
        ("#1", "transaction "),
        ("#2", "sales date"),
    )

    date_from = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    # time_from = forms.TimeField(widget=forms.TimeInput(attrs={"type":"time"}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    result_by = forms.ChoiceField(choices=RESULT_CHOICES)
