from django import forms

from bootstrap_datepicker_plus.widgets import DatePickerInput


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(
            options={
                'format': 'DD.MM.YY',
                'showTodayButton': True,
                'locale': 'ru'
            }
        )
    )
    end_date = forms.DateField(
        widget=DatePickerInput(
            options={
                'format': 'DD.MM.YY',
                'showTodayButton': True,
                'locale': 'ru'
            }
        )
    )
