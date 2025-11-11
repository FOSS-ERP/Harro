import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def create_custom_fields_on_migrate():
    fields = {
        "Timesheet Detail" : [
            {
                "insert_after" : "completed",
                "fieldname" : "employee",
                "label" : "Employee",
                "fieldtype" : "Link",
                "options" : "Employee",
            }
        ]
    }

    create_custom_fields(fields)