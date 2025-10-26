import frappe
from erpnext.manufacturing.report.bom_stock_report.bom_stock_report import get_bom_stock

@frappe.whitelist()
def fetch_row_material(self, method=None):
    """Fetch raw materials and append them to the Work Order"""

    if self.bom_no:
        filters = frappe._dict({
            "bom": self.bom_no,
            "warehouse": "All Warehouses - HH",
            "show_exploded_view" : 0,
            "qty_to_produce" : 1,
            "show_exploded_view" : 1
        })
        report_data = get_bom_stock(filters)

        for row in report_data:
            self.append("wo_raw_material", {
                "item": row[0],
                "item_name": row[1],
                "description": row[2],
                "bom_qty": row[3],
                "bom_uom": row[4],
                "required_qty": row[5],
                "in_stock_qty": row[6],
                "enough_parts_to_build": row[7]
            })
        self.save(ignore_permissions=True)

def enqueue_fetch_row_material(doc, method):
    """Enqueue job to fetch raw materials asynchronously"""
    frappe.enqueue(
        fetch_row_material,
        self=doc,
        queue='long',
        timeout=600,
    )