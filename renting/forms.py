from django import forms
from django.core.exceptions import ValidationError
from datetime import date
current = date.today()


def date_is_current(value):
    global start_date
    start_date = value
    if value.day < current.day or value.month < current.month or value.year < current.year:
        raise forms.ValidationError("Enter the correct Value!")


def date_is_greater_than_start(value):
    if value.day < start_date.day and value.month == start_date.month and value.year == start_date.year:
        raise forms.ValidationError("Enter the correct Value of returning Date!")
    elif value.month < current.month or value.year < current.year:
        raise forms.ValidationError("Enter the correct Value!")


class DateInput(forms.DateInput):
    input_type = 'date'
    format = 'dd/mm/yy'


class RentingOrderForm(forms.Form):
    start = forms.DateField(widget=DateInput, validators=[date_is_current])
    end = forms.DateField(widget=DateInput, validators=[date_is_greater_than_start])

