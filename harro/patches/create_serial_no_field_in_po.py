import frappe

def execute():
    frappe.get_doc({
        "doctype" : "Custom Field",
        "dt" : "Purchase Order Item",
        "insert_after" : "company_total_stock",
        "fieldname" : "serial_nos_section",
        "label" : "Serial Nos",
        "fieldtype" : "Section Break",
        "is_system_generated" : 1
    }).insert()

    frappe.get_doc({
        "doctype" : "Custom Field",
        "dt" : "Purchase Order Item",
        "insert_after" : "serial_nos_section",
        "fieldname" : "serial_no",
        "label" : "Serial No",
        "fieldtype" : "Long Text",
        "is_system_generated" : 1
    }).insert()