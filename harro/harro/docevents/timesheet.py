import frappe
from harro.harro.docevents.project import calculate_timesheet_hours

def on_submit(self, method):
    if self.parent_project:
        calculate_timesheet_hours(self.parent_project)