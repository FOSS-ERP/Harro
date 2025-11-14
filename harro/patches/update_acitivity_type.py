import frappe

def execute():
    fields = {
        "Planned Mechanical Design Hours" : [
            "custom_planned_mechanical_design_hours",
            "custom_mechanical_design_hours"
        ],
        "Planned Controls Engineering Hours" : [
            "custom_planned_controls_engineering_hours",
            "custom_controls_engineering_hours"
        ],
        "Planned Validation Services Hours" : [
            "custom_planned_validation_services_hours_",
            "custom_validation_services_hours"
        ],
        "Planned Technical Document Hours" : [
            "custom_planned_technical_documentation_hours_",
            "custom_technical_documentation_hours"
        ],
        "Project Management Hours" : [
            "custom_planned_project_management_hours_copy",
            "custom_project_management_hours"
        ]
    }

    activity_type_list = frappe.db.get_list("Activity Type", pluck="name")
    for row in activity_type_list:
        if fields.get(row):
            frappe.db.set_value("Activity Type", row, "custom_update_to_project_field", fields.get(row)[0])
            frappe.db.set_value("Activity Type", row, "custom_planned_hours_field_name", fields.get(row)[1])