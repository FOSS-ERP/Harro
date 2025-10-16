import frappe
from openpyxl import load_workbook



@frappe.whitelist()
def extract_bom_item_data(file_path, bom_c):
    doc = frappe.get_doc("BOM Creator", bom_c)

    if not file_path:
        frappe.throw("Please upload a file first.")

    # Read Excel
    public_file_path = frappe.get_site_path("public", file_path.lstrip("/"))
    workbook = load_workbook(filename=public_file_path, data_only=True)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1] if cell.value]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

    create_item_group()

    # Map to track FG item → child table row idx
    fg_row_map = {}

    for row in data:
        artikel = row.get("Artikel")
        baugruppe = row.get("Baugruppe")
        menge = row.get("Menge")

        # Create Item if it doesn't exist
        if not frappe.db.exists("Item", artikel):
            create_item(artikel)
        if not frappe.db.exists("Item", baugruppe):
            create_item(baugruppe)

        new_row = {
            "item_code": artikel,
            "fg_item": baugruppe,
            "qty" : menge
        }

        # Set parent_row_no only if FG item already exists in table
        if baugruppe in fg_row_map:
            new_row["parent_row_no"] = fg_row_map[baugruppe]
        else:
            # Top-level FG item (first occurrence)
            new_row["fg_reference_id"] = doc.name
            new_row["fg_item"] = doc.item_code

        # Append row and store child table index
        doc.append("items", new_row)
        fg_row_map[artikel] = doc.items[-1].idx  # map this item's row index

    doc.save()


def create_item(item):
    frappe.get_doc({
        "doctype" : "Item",
        "item_code" : item,
        "item_group" : "Production Part",
    }).insert()
    
def create_item_group():
    if not frappe.db.exists("Item Group", "Production Part"):
        frappe.get_doc({
            "doctype" : "Item Group",
            "parent_item_group" : "All Item Groups",
            "item_group_name" : "Production Part"
        }).insert()
    

def create_item(item):
    frappe.get_doc({
        "doctype" : "Item",
        "item_code" : item,
        "item_group" : "Production Part",
    }).insert()
    
def create_item_group():
    if not frappe.db.exists("Item Group", "Production Part"):
        frappe.get_doc({
            "doctype" : "Item Group",
            "parent_item_group" : "All Item Groups",
            "item_group_name" : "Production Part"
        }).insert()
    