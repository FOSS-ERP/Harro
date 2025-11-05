import frappe


def execute():
    data = [
            {'name': 'Controls Engineering Hours',
            'custom_update_to_project_field': 'custom_controls_engineering_hours'},
            {'name': 'Technical Documentation Hours',
            'custom_update_to_project_field': 'custom_technical_documentation_hours'},
            {'name': 'Validation Services Hours',
            'custom_update_to_project_field': 'custom_validation_services_hours'},
            {'name': 'Assembly Estimated Hours',
            'custom_update_to_project_field': 'custom_assembly_estimated_hours'},
            {'name': 'Project Management Hours',
            'custom_update_to_project_field': 'custom_project_management_hours'},
            {'name': 'Mechanical Design Hours',
            'custom_update_to_project_field': 'custom_mechanical_design_hours'}
            ]
    for row in data:
        if activity := frappe.db.exists("Activity Type", row.get("name")):
            frappe.db.set_value("Activity Type", activity, "custom_update_to_project_field", row.get("custom_update_to_project_field"))
        else:
            frappe.get_doc(
                {
                "activity_type":f"{row.name}",
                "costing_rate":0,
                "custom_unproductive_work":0,
                "billing_rate":0,
                "disabled":0,
                "custom_update_to_project_field" : f"{row.custom_update_to_project_field}",
                "doctype":"Activity Type",
                "__last_sync_on":"2025-11-05T07:00:05.333Z"
                }
            ).insert()
    