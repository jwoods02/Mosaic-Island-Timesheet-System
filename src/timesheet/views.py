import calendar
import datetime
import json
from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Employee, Activity, Department, MonthControlRecord, RowControl, Entry, BankHoliday
from .forms import RowControlForm, EntryForm


def getDaysInYearMonthList(year, month):
    """
    Returns a formatted list of days in the month
    and the corresponding weekday
    :return:
    """
    day_names = {
        0: 'Mon',
        1: 'Tue',
        2: 'Wed',
        3: 'Thu',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun'
    }
    year = int(year)
    month = int(month)

    # Get the total number of days in the month
    total_days = calendar.monthrange(year, month)[1]

    day_list = []

    # For each day in the month
    for day in range(1, total_days):

        # Make all days 2 digits. (Adds leading zero to 1-9)
        theday = str(day).zfill(2)

        # Get the weekday for that date
        dayofweek = calendar.weekday(year, month, day)

        date = datetime.date(year, month, day)

        try:
            BankHoliday.objects.get(date=date)
            # Format day information for table header for bank holiday
            theday = str(theday) + " <br> " + "B/H"

        except BankHoliday.DoesNotExist:
            # Format day information for table header
            theday = str(theday) + " <br> " + str(day_names[dayofweek])

        # Append formatted information to a list
        day_list.append(theday)

    if month == 2 and calendar.isleap(year):

        theday = 29

        # Get the weekday for that date
        dayofweek = calendar.weekday(year, month, theday)

        str(theday) + " <br> " + str(day_names[dayofweek])

        try:
            BankHoliday.objects.get(date=date)
            # Format day information for table header for bank holiday
            theday = str(theday) + " <br> " + "B/H"

        except BankHoliday.DoesNotExist:
            # Format day information for table header
            theday = str(theday) + " <br> " + str(day_names[dayofweek])

        # Append formatted information to a list
        day_list.append(theday)

    return day_list


def getTableData(month_control_record, year, month):
    """
    Returns a 2 dimensional list formatted as:
        For each row control:
            [Dept, Activity, Notes, Entries or blank columns (upto the last day of the month)]
    :return:
    """
    year = int(year)
    month = int(month)

    # Get the total number of days in the month
    total_days = calendar.monthrange(year, month)[1]

    if month == 2 and calendar.isleap(year):
        total_days += 1

    table_data = []

    # For each row in the month control record
    for row_control in RowControl.objects.filter(month_control_record=month_control_record):
        # Add [Dept, Activity, Notes]
        table_row = [row_control.department, row_control.activity, row_control.notes]

        # For each day in the month
        for day in range(1, total_days):
            # Loop through each day in the month
            date = datetime.date(year, month, day)

            try:
                # Try to find entry for that date
                the_entry = Entry.objects.get(row_control=row_control, date=date)
                # Only select the hours field
                the_entry = the_entry.hours
            except Entry.DoesNotExist:
                # If an entry does not exist for this day set as blank
                the_entry = ""

            # Add entry or blank field to the table row after [Dept, Activity, Notes]
            table_row.append(the_entry)

        # Once all days have been iterated through add the row to the table and loop through next row
        table_data.append(table_row)

    return table_data


def get_month_name(monthcode):
    """
    Returns the month name in plain text from a month code
    :return:
    """
    # Dictionary with month names
    monthdict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

    # Set monthcode to int
    monthcode = int(monthcode)

    # Find month name from the given month code
    monthname = monthdict[monthcode]

    return monthname


def get_month_control_record_list(employee, currentyear, currentmonth):
    """
    Returns list of all month control records for user, with current year selected.
    """
    # Get list of all open mcr's for user, ordered by most recent first
    mcr_list = MonthControlRecord.objects.filter(employee=employee, status=0).order_by('first_day_of_month')

    # Initialise 2d list to store data for list
    year_month_list = []

    # For 0 to number of open mcr's
    for i in range(len(mcr_list)):
        # Append new blank list for each mcr
        year_month_list.append([])

        # Append url into the list for the mcr
        year_month_list[i].append(mcr_list[i].get_year_month_url)

        # Append month and year in text to use as label for menu
        year_month_list[i].append(mcr_list[i].first_day_of_month.strftime("%Y %b"))

        # If the mcr is the one currently open (if url corresponds to list)
        if mcr_list[i].first_day_of_month.year == int(currentyear) and mcr_list[i].first_day_of_month.month == int(currentmonth):
            # Append true to the list for that mcr
            year_month_list[i].append(True)

    return year_month_list


def index_number_of_object(list, object):
    """
    Returns index number for object in a list
    """
    count = 0
    for i in list:
        if i == object:
            return count
        count += 1

##################
# TIMESHEET VIEWS
##################

@login_required
def index(request):

    """
    Finds latest open timesheet and redirects to it
    """
    # Get the employee model for the user signed in
    employee = Employee.objects.get(user=request.user)

    # Get the latest month active for employee
    latest_mcr = MonthControlRecord.objects.filter(employee=employee).order_by('-first_day_of_month')[0]

    print("index list: ", latest_mcr)

    # Select the first_day_of_month attribute
    latest_mcr = latest_mcr.first_day_of_month

    # Create '/year/month/' formatted url to redirect to the monthview view
    redirect_url = '/' + str(latest_mcr.year) + '/' + str(latest_mcr.month) + '/'

    return redirect(redirect_url, permanent=True)


@login_required
def month_view(request, year, month):

    # Get month name in text
    monthname = get_month_name(month)

    # Set page title
    title = str(monthname) + " " + str(year)

    # Get headers for the table
    table_header = getDaysInYearMonthList(year, month)

    # Get the employee model for the user signed in
    employee = Employee.objects.get(user=request.user)

    # Get the first day of the month from URL
    first_day_of_month = datetime.date(int(year), int(month), 1)

    # Get the month_control_record for the user logged in and for the month from URL or error
    try:
        month_control_record = MonthControlRecord.objects.get(employee=employee, first_day_of_month=first_day_of_month)
    except MonthControlRecord.DoesNotExist:
        # TODO CHANGE THIS TO ERROR PAGE
        return redirect('http://127.0.0.1:8000')

    # Initialise forms
    row_control_form = RowControlForm(initial={'month_control_record': month_control_record})
    entry_form = EntryForm()

    # Making form fields hidden
    entry_form.fields['row_control'].widget = forms.HiddenInput()
    entry_form.fields['date'].widget = forms.HiddenInput()

    row_control_form.fields['month_control_record'].widget = forms.HiddenInput()

    # Get table data for the month_control_record
    table_data = getTableData(month_control_record, year, month)

    # Get list of all month control records for user with the current one selected for easy navigation
    year_month_list = get_month_control_record_list(employee, year, month)

    # If user has submitted a form
    if request.is_ajax() and request.method == "POST":
        print("AJAX POST REQUEST")
        print(request.POST)

        # If user submits row_control form
        if 'month_control_record' in str(request.POST):

            print(request.POST)

            instance_pk = request.POST["instance"]

            try:

                if request.POST["delete"] == "True":

                    instance = RowControl.objects.get(pk=instance_pk)

                    for i in Entry.objects.filter(row_control=instance):
                        i.delete()

                    instance.delete()

                return HttpResponse("/")

            except KeyError:

                try:
                    row_control_form = RowControlForm(request.POST, instance=RowControl.objects.get(pk=instance_pk))
                except ValueError:
                    row_control_form = RowControlForm(request.POST)

                if row_control_form.is_valid():
                    row_control_form.save()
                    print("VALID REQUEST")
                    return HttpResponse("/")
                else:
                    row_control_form.fields['month_control_record'].widget = forms.HiddenInput()
                    return render(request, "timesheet/blocks/row_control_form.html", {'row_control_form': row_control_form})

        elif 'hours' in str(request.POST):

            instance_pk = request.POST["instance"]

            try:

                if request.POST["delete"] == "True":

                    instance = Entry.objects.get(pk=instance_pk)

                    instance.delete()

                return HttpResponse("/")

            except KeyError:

                try:
                    entry_form = EntryForm(request.POST, instance=Entry.objects.get(pk=instance_pk))
                except ValueError:
                    entry_form = EntryForm(request.POST)

                if entry_form.is_valid():
                    entry_form.save()
                    return HttpResponse("/")
                else:
                    entry_form.fields['row_control'].widget = forms.HiddenInput()
                    entry_form.fields['date'].widget = forms.HiddenInput()
                    return render(request, "timesheet/blocks/entry_form.html", {'entry_form': entry_form})

        elif 'lock' in str(request.POST):

            print("Lock request:", month_control_record.status)

            # Sets timesheet to closed. Expansion opportunity for 'locked' status.
            month_control_record.status = 2
            month_control_record.save()

    elif request.is_ajax() and request.method == "GET":

        print("AJAX GET REQUEST")

        rawrow = request.GET['row']
        rawday = request.GET['day']

        # Get the employee model for the user signed in
        employee = Employee.objects.get(user=request.user)

        # Get the first day of the month from URL
        first_day_of_month = datetime.date(int(year), int(month), 1)

        # Get the month_control_record for the user logged in and for the month
        month_control_record = MonthControlRecord.objects.get(employee=employee, first_day_of_month=first_day_of_month)

        the_row_control = RowControl.objects.filter(month_control_record=month_control_record)

        if int(rawday) > 0:

            the_row_control = the_row_control[int(rawrow)]

            date = str(year) + '-' + str(month) + '-' + str(rawday)

            try:
                the_entry = Entry.objects.get(row_control=the_row_control, date=date)
                instance = the_entry.pk
                hours = str(the_entry.hours)
            except Entry.DoesNotExist:
                instance = None
                hours = None

            the_row_control = the_row_control.pk

            data = {
                'form': "entry",
                'row_control': the_row_control,
                'date': date,
                'hours': hours,
                'instance': instance,

            }

            data = json.dumps(data)

        else:

            instance = the_row_control[int(rawrow)]

            departments = Department.objects.all()

            departmentno = index_number_of_object(departments, instance.department) + 1

            activites = Activity.objects.all()

            activityno = index_number_of_object(activites, instance.activity) + 1

            notes = instance.notes

            data = {
                'form': "row_control",
                'department': departmentno,
                'activity': activityno,
                'instance': instance.pk,
                'notes': notes,

            }

            data = json.dumps(data)

        return HttpResponse(data)

    context = {
        'title': title,
        'row_control_form': row_control_form,
        'entry_form': entry_form,
        'year': year,
        'month': month,
        'monthname': monthname,
        'table_header': table_header,
        'table_data': table_data,
        'timesheet_list': year_month_list,
    }


    print("DEFAULT PAGE RENDER")
    print(year, month)
    return render(request, "timesheet/monthview.html", context)

##################
# SUMMARY VIEWS
##################


def get_employee_list():
    """
    Returns list of all employees numbers and usernames.
    """
    employee_list = [['', '---------']]

    for employee in Employee.objects.all():

        staff_number = employee.staff_number

        username = employee.user

        employee_list_object = ["/summary/" + str(staff_number), str(staff_number) + " - " + str(username)]

        employee_list.append(employee_list_object)

    print(employee_list)

    return employee_list


@login_required
def options(request):

    title = "Options"

    department_number = len(Department.objects.all())

    activity_number = len(Activity.objects.all())

    employee_number = len(Employee.objects.all())

    practice_area_number = len(Department.objects.filter(type=0))

    employee_list = get_employee_list()

    entry_number = len(Entry.objects.all())

    row_control_number = len(RowControl.objects.all())

    month_control_number = len(MonthControlRecord.objects.all())

    if request.method == "POST":

        print(request.POST)

        if 'open_timesheets' in request.POST:

            open_year = int(request.POST['year'])

            open_month = int(request.POST['month'])

            if 1 > open_month or open_month > 12:
                return HttpResponse("Please choose a valid month between 1 and 12")
            elif open_year < 2015:
                return HttpResponse("Please choose a year during or after 2015")

            open_date = datetime.date(open_year, open_month, 1)

            new_mcr_count = 0

            for employee in Employee.objects.filter(active=True):

                try:
                    MonthControlRecord.objects.get(employee=employee, first_day_of_month=open_date)
                except MonthControlRecord.DoesNotExist:
                    new_mcr = MonthControlRecord(employee=employee, first_day_of_month=open_date)
                    new_mcr.save()

                    new_mcr_count += 1

            return HttpResponse("Month opened. " + str(new_mcr_count) + " timesheets created.")

        return HttpResponse()

    context = {
        'title': title,
        'dept_no': department_number,
        'act_no': activity_number,
        'employee_no': employee_number,
        'practice_area_no': practice_area_number,
        'employee_list': employee_list,
        'entry_no': entry_number,
        'row_control_no': row_control_number,
        'month_control_no': month_control_number,
    }

    return render(request, 'timesheet/options.html', context)


@login_required
def summary_month(request, year, month):

    year = str(year)

    month = str(month)

    return HttpResponse("SUMMARY MONTH " + year + " " + month)


@login_required
def summary_activities(request):

    return HttpResponse("SUMMARY ACTIVITIES")


@login_required
def summary_departments(request):

    return HttpResponse("SUMMARY DEPARTMENTS")


@login_required
def summary_employees(request, employee):

    employee = str(employee)

    return HttpResponse("SUMMARY EMPLOYEES" + " " + employee)