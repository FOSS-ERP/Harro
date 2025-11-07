import frappe

@frappe.whitelist()
def get_bin_location(rack):
    frappe.throw(str(rack))