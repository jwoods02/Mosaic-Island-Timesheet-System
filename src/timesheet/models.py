from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_number = models.IntegerField(unique=True, primary_key=True)
    practice_area = models.ForeignKey('Department', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user)


@python_2_unicode_compatible
class Department(models.Model):
    TYPE_CHOICES = (
        (0, 'Practice area'),
        (1, 'Client'),
        (2, 'Managed delivery'),
    )
    name = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    type = models.IntegerField(choices=TYPE_CHOICES)

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class Activity(models.Model):
    name = models.CharField(max_length=64, unique=True)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


@python_2_unicode_compatible
class MonthControlRecord(models.Model):
    STATUS_CHOICES = (
        (0, 'Open'),
        (1, 'Locked'),
        (2, 'Closed'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    first_day_of_month = models.DateField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    @property
    def get_year_month(self):
        return str(self.first_day_of_month.year) + "/" + str(self.first_day_of_month.month)

    def __str__(self):
        return "Employee: " + str(self.employee) + " - " + str(self.first_day_of_month)


@python_2_unicode_compatible
class RowControl(models.Model):
    month_control_record = models.ForeignKey(MonthControlRecord, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    notes = models.CharField(max_length=200)

    def __str__(self):
        return str(self.pk) + " MCR[ " + str(self.month_control_record) + " ]"


@python_2_unicode_compatible
class Entry(models.Model):
    row_control = models.ForeignKey(RowControl, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return "Row control: " + str(self.row_control.pk) + "  Date : " + str(self.date) + " Hours: " + str(self.hours)


@python_2_unicode_compatible
class BankHoliday(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self):
        return str(self.date)