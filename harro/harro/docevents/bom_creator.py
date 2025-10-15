import frappe
from openpyxl import load_workbook

@frappe.whitelist()
def extract_bom_item_data(file_path):
    if not file_path:
        frappe.throw("Please upload a file first.")
    
    public_file_path = frappe.get_site_path("public", file_path.lstrip("/"))
    workbook = load_workbook(filename=public_file_path, data_only=True)
    sheet = workbook.active  # read first sheet
    