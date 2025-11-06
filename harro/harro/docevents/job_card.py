import frappe
from harro.harro.docevents.project import calculate_project_working_hours


def validate(self, method):
    if self.project:
        calculate_project_working_hours(self.project)

def on_submit(self, method):
    if self.project:
        calculate_project_working_hours(self.project)

def on_cancel(self, method):
    if self.project:
        calculate_project_working_hours(self.project)