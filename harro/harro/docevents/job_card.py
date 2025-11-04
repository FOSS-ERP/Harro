import frappe
from harro.harro.docevents.project import calculate_project_working_hours


def on_submit(self, method):
    calculate_project_working_hours(self.project)