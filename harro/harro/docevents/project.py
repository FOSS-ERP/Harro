import frappe
from frappe.utils import flt


import frappe

def calculate_project_working_hours(project):
    # Get all submitted job cards for the project
    job_cards = frappe.db.get_all(
        "Job Card",
        filters={"project": project, "docstatus": 1},
        fields=["name", "operation", "total_time_in_mins"]
    )

    # Dictionary to hold operation-wise total minutes
    operation_wise_time = {}

    for jc in job_cards:
        operation = jc.operation or "Unknown"
        total_time_in_mins = flt(jc.total_time_in_mins) or 0

        # Sum total time for each operation
        operation_wise_time[operation] = flt(operation_wise_time.get(operation, 0)) + total_time_in_mins
    
    current_actule_manufacturing_hours = frappe.db.get_value("Project", project, "actual_manufacturing_hours") or 0

    if operation_wise_time.get("Mechanical Operation"):
        frappe.db.set_value("Project", project, "actual_mechanical_assembly", operation_wise_time.get("Mechanical Operation"))
        
    if operation_wise_time.get("Electrical Operation"):
        frappe.db.set_value("Project", project, "actual_electrical_assembly", operation_wise_time.get("Electrical Operation"))
    
    actual_mechanical_assembly = flt(operation_wise_time.get("Mechanical Operation")) or 0
    actual_electrical_assembly = flt(operation_wise_time.get("Electrical Operation")) or 0

    current_actule_manufacturing_hours = flt(actual_mechanical_assembly) + flt(actual_electrical_assembly) + flt(current_actule_manufacturing_hours)

    frappe.db.set_value("Project", project, "actual_manufacturing_hours", current_actule_manufacturing_hours)
    


    

import frappe

@frappe.whitelist()
def get_effort_data(project):
    """Return planned and actual hours for all 3 categories."""
    fields = [
        "planned_manufacturing_hours",
        "actual_manufacturing_hours",
        "planned_mechanical_assembly",
        "actual_mechanical_assembly",
        "planned_electrical_assembly",
        "actual_electrical_assembly",
    ]

    data = frappe.db.get_value("Project", project, fields, as_dict=True) or {}

    return {
        "planned_manufacturing_hours": data.get("planned_manufacturing_hours", 0),
        "actual_manufacturing_hours": data.get("actual_manufacturing_hours", 0),
        "planned_mechanical_assembly": data.get("planned_mechanical_assembly", 0),
        "actual_mechanical_assembly": data.get("actual_mechanical_assembly", 0),
        "planned_electrical_assembly": data.get("planned_electrical_assembly", 0),
        "actual_electrical_assembly": data.get("actual_electrical_assembly", 0),
    }

