import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    meta = frappe.get_meta('Job Card')
    if meta.has_field("custom_timesheet"):
        frappe.db.delete("Custom Field", "Job Card-custom_timesheet")
    
    fields = {
        "Timesheet Detail" : [
            {
                "fieldname" : "reference",
                "fieldtype" : "Link",
                "label" : "Reference",
                "options" : "Timesheet",
                "depends_on" : "eval:parent.doctype == 'Job Card'",
                "read_only" : 1,
                "no_copy" : 1
            }
        ]
    }
    create_custom_fields(fields)

