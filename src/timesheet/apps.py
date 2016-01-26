from django.apps import AppConfig


class TimesheetConfig(AppConfig):
    # Sets name for django admin
    name = 'timesheet'

    def ready(self):
        # Loads signals.py file
        import timesheet.signals