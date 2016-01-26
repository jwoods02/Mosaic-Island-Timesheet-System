from django import forms

from .models import RowControl, Entry, Department, Activity


class RowControlForm(forms.ModelForm):
    class Meta:
        model = RowControl
        fields = ['month_control_record', 'department', 'activity', 'notes']


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['row_control', 'date', 'hours']

    def clean(self):
        cleaned_data = self.cleaned_data

        row_control = cleaned_data['row_control']

        date = cleaned_data['date']

        hours = cleaned_data['hours']

        if not self.instance:
            if Entry.objects.get(row_control=row_control, date=date):
                raise forms.ValidationError("Entry for this day and row already exists.")

        if hours > 24:
            raise forms.ValidationError("Cannot work more than 24 hours in a day.")

        if hours <= 0:
            raise forms.ValidationError("Hours field must be more than 0.")

        # Always return cleaned data
        return cleaned_data

