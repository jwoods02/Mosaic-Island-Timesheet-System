import calendar, datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Employee, MonthControlRecord, RowControl, Entry
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
    for i in range (1, total_days):

        # Make all days 2 digits. (Adds leading zero to 1-9)
        theday = str(i).zfill(2)

        # Get the weekday for that date
        dayofweek = calendar.weekday(year, month, i)

        theday = str(theday) + " <br> " + str(day_names[dayofweek])

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
            except:
                # If an entry does not exist for this day set as blank
                the_entry = ""

            # Add entry or blank field to the table row after [Dept, Activity, Notes]
            table_row.append(the_entry)

        # Once all days have been iterated through add the row to the table and loop through next row
        table_data.append(table_row)

    return table_data


@login_required
def index(request, year, month):
    title = 'Index'

    # Initialise forms
    row_control_form = RowControlForm()
    entry_form = EntryForm()

    # Get headers for the table
    table_header = getDaysInYearMonthList(year, month)

    # Get the employee model for the user signed in
    employee = Employee.objects.get(user=request.user)

    # Get the first day of the month from URL
    first_day_of_month = datetime.date(int(year), int(month), 1)

    # Get the month_control_record for the user logged in and for the month from URL
    month_control_record = MonthControlRecord.objects.get(employee=employee, first_day_of_month=first_day_of_month)

    # Get table data for the month_control_record
    table_data = getTableData(month_control_record, year, month)

    context = {
        'title': title,
        'row_control_form': row_control_form,
        'entry_form': entry_form,
        'year': year,
        'month': month,
        'table_header': table_header,
        'month_control_record': month_control_record.pk,
        'table_data': table_data,
    }

    # If user has submitted a form
    if request.method == 'POST':

        # If user submits row_control form
        if 'row_control_submit' in request.POST:

            # Recognise the data submitted by user
            row_control_form = RowControlForm(request.POST)

            if row_control_form.is_valid():
                row_control_form.save()

        elif 'entry_submit' in request.POST:

            # Recognise the data submitted by user
            entry_form = EntryForm(request.POST)

            if entry_form.is_valid():
                entry_form.save()

    return render(request, "timesheet/index.html", context)


@login_required
def form_design(request):
    title = 'form design'
    context = {
        title: 'title',
    }
    return render(request, "timesheet/formdesign.html", context)


@login_required
def test_form(request):
    title = 'test form'
    row_control_form = RowControlForm()
    entry_form = EntryForm()

    context = {
        'title': title,
        'row_control_form': row_control_form,
        'entry_form': entry_form,
    }

    if request.method == 'POST':
        if 'row_control_submit' in request.POST:
            row_control_form = RowControlForm(request.POST)
            if row_control_form.is_valid():
                row_control_form.save()

        elif 'entry_submit' in request.POST:
            entry_form = EntryForm(request.POST)
            if entry_form.is_valid():
                entry_form.save()

    return render(request, "timesheet/test_form.html", context)
