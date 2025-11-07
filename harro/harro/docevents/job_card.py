import frappe
import json
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


@frappe.whitelist()
def update_unproductive_log(arg, job_card):
    args = json.loads(arg)
    doc = frappe.get_doc("Job Card", job_card)
    doc.append("custom_unproductive_work_timelogs", {
        "activity_type" : args.get("activity_type"),
        "from_time" : args.get("from_time"),
        "project" : args.get("project"),
        "task" : args.get("task")
    })
    doc.flags.ignore_permissions= True
    doc.save()

@frappe.whitelist()
def resume_unproductive_log(to_time, job_card):
    doc = frappe.get_doc("Job Card", job_card)
    doc.custom_unproductive_work_timelogs[-1].to_time = to_time
    doc.flags.ignore_permissions = True

    row = doc.custom_unproductive_work_timelogs[-1]

    timesheet_doc= frappe.get_doc({
        "doctype" : "Timesheet",
        "parent_project" : doc.project,
        "company" : doc.company,
        "time_logs" : [
            {
                "activity_type" : row.get("activity_type"),
                "from_time" : row.get("from_time"),
                "to_time" : row.get("to_time"),
                "project" : doc.project,
                "task" : row.get("task")
            }
        ]
    })
    timesheet_doc.flags.ignore_permissions = True
    timesheet_doc.insert()
    timesheet_doc.submit()
    doc.custom_unproductive_work_timelogs[-1].reference = timesheet_doc.name
    doc.save()
