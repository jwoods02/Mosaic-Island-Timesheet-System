from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MonthControlRecord, RowControl, Activity


# Code runs after a new MonthControlRecord is saved.
@receiver(post_save, sender=MonthControlRecord)
def add_default_activity_rows_to_new_month_control_record(sender, **kwargs):

    #Selects the MonthControlRecord being created
    instance = kwargs['instance']

    #If MonthControlRecord being saved is new or 'being created'
    if kwargs['created']:
        # Find the employee the MonthControlRecord is for
        employee = instance.employee

        # Find the practice area of that employee (to set the department to)
        practice_area = employee.practice_area

        # For each default activity in the database
        for activity in Activity.objects.filter(default=True):

            # Make new Row_Control inside the new MonthControlRecord for this activity with the employee's practice area as department
            new_row_control = RowControl(month_control_record=instance, department=practice_area, activity=activity)

            # Save the new row_control
            new_row_control.save()
