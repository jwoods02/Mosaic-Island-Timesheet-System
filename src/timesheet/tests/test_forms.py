import datetime

from django.test import TestCase

from timesheet.models import *
from timesheet.forms import RowControlForm, EntryForm


def fullsave(i):
    """
    Cleans and saves i
    :return:
    """
    i.full_clean()
    return i.save()


class RowControlFormTests(TestCase):
    def setUp(self):
        """
        Uses previous test code to set up basic models.
        If NewBasicModelTests() in test_models.py changes this also needs to be changed.
        :return:
        """
        u = User.objects.create_user('test', 'test@gmail.com', '00Password')
        fullsave(u)
        d = Department(name="Test dept", type=0)
        fullsave(d)
        a = Activity(name="Test activity")
        fullsave(a)
        e = Employee(user=u, staff_number="0001", practice_area=d)
        fullsave(e)
        bh = BankHoliday(date=datetime.date(2015, 12, 25))
        fullsave(bh)
        employee = Employee.objects.get(staff_number="1")
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord(employee=employee, first_day_of_month=thedate)
        fullsave(mcr)

    def test_valid_row_control_form(self):
        """
        Should return new record for the valid form.
        :return:
        """
        employee = Employee.objects.get(staff_number="1")
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord.objects.get(employee=employee, first_day_of_month=thedate)
        d = Department.objects.get(name="Test dept")
        a = Activity.objects.get(name="Test activity")
        form = RowControlForm({
            'month_control_record': mcr.pk,
            'department': d.pk,
            'activity': a.pk,
            'notes': "Test notes",
        })
        self.assertTrue(form.is_valid())
        savedform = form.save()
        self.assertEqual(savedform.month_control_record, mcr)
        self.assertEqual(savedform.department, d)
        self.assertEqual(savedform.activity, a)
        self.assertEqual(savedform.notes, "Test notes")

    def test_non_unique_row_control_form(self):
        """
        Should set up valid data for first RowControl,
        then error for the second as not unique,
        then valid for third as notes changed.
        :return:
        """
        employee = Employee.objects.get(staff_number="1")
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord.objects.get(employee=employee, first_day_of_month=thedate)
        d = Department.objects.get(name="Test dept")
        a = Activity.objects.get(name="Test activity")
        form = RowControlForm({
            'month_control_record': mcr.pk,
            'department': d.pk,
            'activity': a.pk,
            'notes': "Test notes",
        })
        self.assertTrue(form.is_valid())
        form.save()
        form = RowControlForm({
            'month_control_record': mcr.pk,
            'department': d.pk,
            'activity': a.pk,
            'notes': "Test notes",
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['This row already exists']})
        form = RowControlForm({
            'month_control_record': mcr.pk,
            'department': d.pk,
            'activity': a.pk,
            'notes': "Test notes 2",
        })
        self.assertTrue(form.is_valid())


class EntryFormTests(TestCase):
    def setUp(self):
        """
        Uses previous test code to set up basic models.
        If NewComplexModelTests() in test_models.py changes this also needs to be changed.
        :return:
        """
        u = User.objects.create_user('test', 'test@gmail.com', '00Password')
        fullsave(u)
        d = Department(name="Test dept", type=0)
        fullsave(d)
        a = Activity(name="Test activity")
        fullsave(a)
        e = Employee(user=u, staff_number="0001", practice_area=d)
        fullsave(e)
        bh = BankHoliday(date=datetime.date(2015, 12, 25))
        fullsave(bh)
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord(employee=e, first_day_of_month=thedate)
        fullsave(mcr)
        rc = RowControl(month_control_record=mcr, department=d, activity=a, notes="test notes")
        fullsave(rc)

    def test_valid_entry_form(self):
        """
        Should return new record for valid form
        :return:
        """
        employee = Employee.objects.get(staff_number="1")
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord.objects.get(employee=employee, first_day_of_month=thedate)
        rc = RowControl.objects.get(month_control_record=mcr, notes="test notes", activity=1, department=1)
        thedate = datetime.date(2015, 12, 12)
        hours = 7.25

        form = EntryForm({
            'row_control': rc.pk,
            'date': thedate,
            'hours': hours
        })
        print(form.errors)
        self.assertTrue(form.is_valid())
        savedform = form.save()
        self.assertEqual(savedform.row_control, rc)
        self.assertEqual(savedform.date, thedate)
        self.assertEqual(savedform.hours, hours)

    def test_non_unique_entry_form(self):
        """
        Should set up valid data for first Entry,
        then error for the second as not unique,
        then valid for third as notes changed.
        :return:
        """
        employee = Employee.objects.get(staff_number="1")
        thedate = datetime.date(2015, 12, 1)
        mcr = MonthControlRecord.objects.get(employee=employee, first_day_of_month=thedate)
        rc = RowControl.objects.get(month_control_record=mcr, notes="test notes", activity=1, department=1)
        thedate = datetime.date(2015, 12, 12)
        hours = 7.25
        form = EntryForm({
            'row_control': rc.pk,
            'date': thedate,
            'hours': hours
        })
        self.assertTrue(form.is_valid())
        form.save()
        hours = 5
        form = EntryForm({
            'row_control': rc.pk,
            'date': thedate,
            'hours': hours
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'__all__': ['This entry already exists']})
        thedate = datetime.date(2015, 12, 13)
        form = EntryForm({
            'row_control': rc.pk,
            'date': thedate,
            'hours': hours
        })
        self.assertTrue(form.is_valid())
