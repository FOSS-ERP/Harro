import frappe

def execute():
    frappe.get_doc({
        "doctype" : "Custom Field",
        "dt" : "Work Order",
        "insert_after" : "required_items",
        "fieldname" : "wo_raw_material",
        "label" : "Raw Material",
        "fieldtype" : "Table",
        "options" : "Work Order Raw Material",
        "is_system_generated" : 1
    }).insert()