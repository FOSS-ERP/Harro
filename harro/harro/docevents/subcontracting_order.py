import frappe
from frappe.utils import flt
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def make_subcontracting_receipt(source_name, target_doc=None):
	return get_mapped_subcontracting_receipt(source_name, target_doc)


def get_mapped_subcontracting_receipt(source_name, target_doc=None):
	def update_item(source, target, source_parent):
		target.purchase_order = source_parent.purchase_order
		target.purchase_order_item = source.purchase_order_item
		target.qty = flt(source.qty) - flt(source.received_qty)
		target.amount = (flt(source.qty) - flt(source.received_qty)) * flt(source.rate)
		target.use_serial_batch_fields = 1

	target_doc = get_mapped_doc(
		"Subcontracting Order",
		source_name,
		{
			"Subcontracting Order": {
				"doctype": "Subcontracting Receipt",
				"field_map": {
					"supplier_warehouse": "supplier_warehouse",
					"set_warehouse": "set_warehouse",
				},
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"Subcontracting Order Item": {
				"doctype": "Subcontracting Receipt Item",
				"field_map": {
					"name": "subcontracting_order_item",
					"parent": "subcontracting_order",
					"bom": "bom",
					"serial_no" : "serial_no"
				},
				"postprocess": update_item,
				"condition": lambda doc: abs(doc.received_qty) < abs(doc.qty),
			},
		},
		target_doc,
	)

	return target_doc