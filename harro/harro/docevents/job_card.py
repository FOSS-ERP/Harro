import frappe
import json
from harro.harro.docevents.project import calculate_project_working_hours
from frappe.utils import (
	get_datetime,
)


def validate(self, method):
    if self.project and not self.is_new():
        calculate_project_working_hours(self.project)

def on_submit(self, method):
    if self.project:
        calculate_project_working_hours(self.project)
    submit_timesheet(self)

def on_cancel(self, method):
    if self.project:
        calculate_project_working_hours(self.project)
    
def submit_timesheet(self):
    time_sheets = []
    for row in self.custom_unproductive_work_timelogs:
        if row.reference not in time_sheets:
            time_sheets.append(row.reference)
    
    for row in time_sheets:
        doc = frappe.get_doc("Timesheet", row)
        doc.flags.ignore_permissions = True
        doc.submit()

@frappe.whitelist()
def update_unproductive_log(arg, job_card):
    args = json.loads(arg)
    doc = frappe.get_doc("Job Card", job_card)
    employees = args.get("employee")
    for row in employees:
        doc.append("custom_unproductive_work_timelogs", {
            "activity_type" : args.get("activity_type"),
            "from_time" : args.get("from_time"),
            "project" : args.get("project"),
            "task" : args.get("task"),
            "employee" : row.get("employee")
        })
    doc.flags.ignore_permissions= True
    doc.save()

@frappe.whitelist()
def resume_unproductive_log(to_time, job_card, employees):
    doc = frappe.get_doc("Job Card", job_card)
    doc.flags.ignore_permissions = True

    employees = json.loads(employees)

    employee_list = [
        row.get("employee") for row in employees
    ]

    
    
    for row in doc.custom_unproductive_work_timelogs:
        if row.employee in employee_list and not row.to_time:
            if row.reference:
                timesheet_doc = frappe.get_doc("Timesheet", row.reference)
                timesheet_doc.append("time_logs", {
                    "activity_type" : row.activity_type,
                    "from_time" : row.from_time,
                    "to_time" : to_time,
                    "project" : doc.project,
                    "task" : row.task,
                    "expected_hours" : row.expected_hours
                })
                timesheet_doc.flags.ignore_permissions= True
                timesheet_doc.save()
            else:
                timesheet_doc = frappe.new_doc("Timesheet")
                timesheet_doc.company = doc.company
                timesheet_doc.parent_project = doc.project
                timesheet_doc.job_card = doc.name,
                timesheet_doc.employee = row.employee
                timesheet_doc.append("time_logs", {
                    "activity_type" : row.activity_type,
                    "from_time" : row.from_time,
                    "to_time" : to_time,
                    "project" : doc.project,
                    "task" : row.task,
                    "expected_hours" : row.expected_hours
                })
                timesheet_doc.flags.ignore_permissions= True
                timesheet_doc.insert()
                row.reference = timesheet_doc.name

            row.to_time = to_time
            from_time = get_datetime(row.from_time)
            to_time = get_datetime(to_time)
            time_difference = to_time - from_time
            hours = time_difference.total_seconds() / 3600
            row.hours = hours

    doc.save()
