import frappe

def execute():
    item_groups = [
        { "german_name" : "Maschine", "indian_name" : "Machine" },
        { "german_name" : "EPLAN_Projekt", "indian_name" : "EPLAN_Project" },
        { "german_name" : "Hauptbaugruppe", "indian_name" : "Main assembly" },
        { "german_name" : "B-Baugruppe", "indian_name" : "B-assembly" },
        { "german_name" : "Funktionsbaugruppe", "indian_name" : "Functional Assembly" },
        { "german_name" : "Station", "indian_name" : "Station" },
        { "german_name" : "Kaufteil", "indian_name" : "Purchase Part" },
        { "german_name" : "Fertigungsteil", "indian_name" : "Manufactured Part" },
    ]

    for row in item_groups:
        if frappe.db.exists("Item Group", row.get("indian_name")):
            frappe.db.set_value("Item Group", row.get("indian_name"), "custom_german_name_of_item_group", row.get("german_name"))
        else:
            frappe.get_doc(
                {
                    "item_group_name": row.get("indian_name"),
                    "custom_german_name_of_item_group" : row.get("german_name"),
                    "parent_item_group": "All Item Groups",
                    "old_parent": "All Item Groups",
                    "doctype": "Item Group"
                }
            ).insert()