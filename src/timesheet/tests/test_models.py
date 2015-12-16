import datetime

from django.test import TestCase

from timesheet.models import *

def fullsave(i):
    """
    Cleans and saves i
    :return:
    """
    i.full_clean()
    return i.save()


class NewBasicModelTests(TestCase):
    def setUp(self):
        """
        Should set up new base user
        :return:
        """
        newUser = User.objects.create_user('test', 'test@gmail.com', '00Password')
        fullsave(newUser)
        self.assertEqual(newUser.username, 'test')

    def test_new_valid_department(self):
        """
        Should set up new active department
        :return:
        """
        d = Department(name="Test dept", type=0)
        fullsave(d)
        self.assertEqual(d.name, "Test dept")
        self.assertEqual(d.type, 0)
        self.assertEqual(d.active, True)

    def test_new_valid_activity(self):
        """
        Should set up new non-default activity
        :return:
        """
        a = Activity(name="Test activity")
        fullsave(a)
        self.assertEqual(a.name, "Test activity")
        self.assertEqual(a.active, True)
        self.assertEqual(a.default, False)

    def test_new_valid_employee(self):
        """
        Should set up new employee from setUp() user and
        uses test_new_valid_department() code to create dept
        :return:
        """
        user = User.objects.get(username="test")
        practice_area = Department(name="Test dept", type=0)
        fullsave(practice_area)
        e = Employee(user=user, staff_number="0001", practice_area=practice_area,)
        fullsave(e)
        self.assertEqual(e.user, user)
        self.assertEqual(e.staff_number, 1)
        self.assertEqual(e.practice_area, practice_area)

    def test_new_bank_holiday(self):
        """
        Should create new bank holiday with date as primary key
        :return:
        """
        theDate = datetime.date(2015, 12, 25)
        bh = BankHoliday(date=theDate)
        fullsave(bh)
        self.assertEqual(bh.date, theDate)
        self.assertEqual(bh.pk, theDate)


class NewComplexModelTests(TestCase):
    def setUp(self):
        """
        Uses previous test code to set up basic models. If NewBasicModelTests() changes
        this also needs to be changed.
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

    def test_new_month_control_record(self):
        """
        Should set up new month control record for test user for
        December 2015 as open.
        :return:
        """
        employee = Employee.objects.get(staff_number="0001")
        theDate = '2015-12-25'
        mcr = MonthControlRecord(employee=employee, first_day_of_month=theDate)
        fullsave(mcr)
        mcrYearMonth = mcr.get_year_month
        self.assertEqual(mcr.employee, employee)
        self.assertEqual(mcr.first_day_of_month, datetime.date(2015, 12, 25))
        self.assertEqual(mcrYearMonth, "2015/12")

    def test_new_row_control(self):
        """
        Should set up new row control for a given month control record
        :return:
        """
        d = Department.objects.get(name="Test dept")
        a = Activity.objects.get(name="Test activity")
        employee = Employee.objects.get(staff_number="0001")
        theDate = datetime.date(2015, 12, 25)
        mcr = MonthControlRecord(employee=employee, first_day_of_month=theDate)
        fullsave(mcr)
        rc = RowControl(month_control_record=mcr, department=d, activity=a, notes="test notes")
        fullsave(rc)
        self.assertEqual(rc.month_control_record, mcr)
        self.assertEqual(rc.department, d)
        self.assertEqual(rc.notes, "test notes")

    def test_new_entry(self):
        """
        Should make new entry for a given row control
        :return:
        """
        d = Department.objects.get(name="Test dept")
        a = Activity.objects.get(name="Test activity")
        employee = Employee.objects.get(staff_number="0001")
        theDate = datetime.date(2015, 12, 25)
        mcr = MonthControlRecord(employee=employee, first_day_of_month=theDate)
        fullsave(mcr)
        rc = RowControl(month_control_record=mcr, department=d, activity=a, notes="test notes")
        fullsave(rc)
        theEntry = Entry(row_control=rc, date=datetime.date(2015, 12, 4), hours=4.25)
        fullsave(theEntry)
        self.assertEqual(theEntry.row_control, rc)
        self.assertEqual(theEntry.date, datetime.date(2015, 12, 4))
        self.assertEqual(theEntry.hours, 4.25)

