import frappe
from erpnext.manufacturing.doctype.bom_creator.bom_creator import BOMCreator
from frappe import _

class CustomBOMCreator(BOMCreator):
	@frappe.whitelist()
	def enqueue_create_boms(self):
		frappe.enqueue(
			self.create_boms,
			queue="long",
			timeout=7200,
			is_async=True,
		)

		frappe.msgprint(
			_("BOMs creation has been enqueued, kindly check the status after some time"), alert=True
		)