from django import forms

from django.core.exceptions import ValidationError

from .models import RowControl, Entry


class RowControlForm(forms.ModelForm):
    class Meta:
        model = RowControl
        fields = ['month_control_record', 'department', 'activity', 'notes']

    def clean(self):
        cleaned_data = self.cleaned_data

        # Ensures row is unique
        try:
            RowControl.objects.get(month_control_record=cleaned_data['month_control_record'],
                                   department=cleaned_data['department'],
                                   activity=cleaned_data['activity'],
                                   notes=cleaned_data['notes'])

        except RowControl.DoesNotExist:
            pass

        else:
            raise ValidationError('This row already exists')

        print("ERRORS:", self.errors)

        # Always return cleaned data
        return cleaned_data


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['row_control', 'date', 'hours']

    def clean(self):
        cleaned_data = self.cleaned_data

        # Ensures data is unique (only 1 hours entry for each date and row_control)
        try:
            Entry.objects.get(row_control=cleaned_data['row_control'],
                              date=cleaned_data['date'])

        except Entry.DoesNotExist:
            pass

        else:
            raise ValidationError('An entry for this date already exists')

        # Always return cleaned data
        return cleaned_data

