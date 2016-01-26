from django.contrib import admin
from .models import *
from .forms import RowControlForm, EntryForm


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'staff_number', 'user', 'practice_area', 'active']

    class Meta:
        model = Employee

admin.site.register(Employee, EmployeeAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'active', 'type']

    class Meta:
        model = Department

admin.site.register(Department, DepartmentAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'active', 'default']

    class Meta:
        model = Activity

admin.site.register(Activity, ActivityAdmin)


class MonthControlRecordAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'employee', 'first_day_of_month', 'status']

    class Meta:
        model = MonthControlRecord

admin.site.register(MonthControlRecord, MonthControlRecordAdmin)



class RowControlAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'month_control_record', 'department', 'activity', 'notes' ]
    form = RowControlForm

admin.site.register(RowControl, RowControlAdmin)


class EntryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'row_control', 'date', 'hours']
    form = EntryForm

admin.site.register(Entry, EntryAdmin)


admin.site.register(BankHoliday)
