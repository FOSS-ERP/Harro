frappe.ui.form.on("BOM Creator", {
	custom_add_bom_items : function(frm){
        frappe.call({
            method: "harro.harro.docevents.bom_creator.extract_bom_item_data",
            args: { 
                file_path : frm.doc.custom_input_bom_file,
                bom_c : frm.doc.name
            },
            freeze: true,
			freeze_message: __("Please wait it will take some time ..."),
            callback(r) {
                if (r.message) {
                    
                }
            }
        });
    }
});