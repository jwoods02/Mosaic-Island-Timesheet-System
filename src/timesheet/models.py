from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class Employee(models.Model):

    # Links to a user from built in django auth
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add staff numbers already part of MI system
    staff_number = models.IntegerField(unique=True, primary_key=True)

    # 'Department' the employee belongs to. Used for default activities
    practice_area = models.ForeignKey('Department', on_delete=models.CASCADE)

    # If active new timesheets created for user
    active = models.BooleanField(default=True)

    # When object 'name' as string called this function called.
    def __str__(self):
        return str(self.user)


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class Department(models.Model):

    # Choices for 'type' field
    TYPE_CHOICES = (
        (0, 'Practice area'),
        (1, 'Client'),
        (2, 'Managed delivery'),
    )

    # Name of department. Must be unique
    name = models.CharField(max_length=40, unique=True)

    # Type of department. Used for practice area selection and could be used for managed delivery extensions
    type = models.IntegerField(choices=TYPE_CHOICES)

    # If active it an be selected on timesheets
    active = models.BooleanField(default=True)

    # When object 'name' as string called this function called.
    def __str__(self):
        return str(self.name)


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class Activity(models.Model):

    # Name for activity
    name = models.CharField(max_length=40, unique=True)

    # If active it an be selected on timesheets
    active = models.BooleanField(default=True)

    # If default, this activity will be added to all new timesheets.
    default = models.BooleanField(default=False, help_text="Adds activity to the top of every new timesheet.")

    # When object 'name' as string called this function called.
    def __str__(self):
        return str(self.name)


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class MonthControlRecord(models.Model):

    # Options for 'status' field
    STATUS_CHOICES = (
        (0, 'Open'),
        # Locked not currently used. Opportunity for expansion to check timesheets.
        (1, 'Locked'),
        (2, 'Closed'),
    )

    # Employee the timesheet is linked to
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    # Month the timesheet is for (first day is used so DateField features can be used)
    first_day_of_month = models.DateField()

    # Timesheet can only be edited if status is 0 or "Open"
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    # Returns a URL to access the month_control_record formatted (year/month)
    @property
    def get_year_month_url(self):
        return "/" + str(self.first_day_of_month.year) + "/" + str(self.first_day_of_month.month) + "/"

    # When object 'name' as string called this function called.
    def __str__(self):
        return "Employee: " + str(self.employee) + " - " + str(self.first_day_of_month)


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class RowControl(models.Model):

    # Month control the Row refers to
    month_control_record = models.ForeignKey(MonthControlRecord, on_delete=models.CASCADE)

    # Department object for the row
    department = models.ForeignKey('Department', on_delete=models.CASCADE)

    # Activity object for the row
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)

    # Notes for the row
    notes = models.CharField(max_length=40, blank=True)

    # When object 'name' as string called this function called.
    def __str__(self):
        return str(self.pk) + " MCR[ " + str(self.month_control_record) + " ]"


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class Entry(models.Model):

    # Row_Control object the Entry refers to
    row_control = models.ForeignKey(RowControl, on_delete=models.CASCADE)

    # Date for the entry
    date = models.DateField()

    # Hours the entry is for
    hours = models.DecimalField(max_digits=4, decimal_places=2)

    # When object 'name' as string called this function called.
    def __str__(self):
        return "Row control: " + str(self.row_control.pk) + "  Date : " + str(self.date) + " Hours: " + str(self.hours)


# Converts __str__ to __unicode__ if python2
@python_2_unicode_compatible
class BankHoliday(models.Model):
    # Date of the bank holiday. Also used as primary key.
    date = models.DateField(primary_key=True)

    # When object 'name' as string called this function called.
    def __str__(self):
        return str(self.date)