frappe.ui.form.on("Purchase Receipt", {
    refresh: function (frm) {
       
	},
    items_on_form_rendered(frm){
       
    }
})

frappe.ui.form.on('Purchase Receipt Item', {
    rack(frm, cdt, cdn) {
        let count = 0 
        setInterval(() => {
            if (count < 6){
                frm.set_query("bin_location", "items", function () {
                    let child = locals[cdt][cdn];
                    return {
                        filters: {
                            rack_name: child.rack
                        },
                    };
                });
                frm.refresh_field('items');
                count++;
            }
        }, 100);
        // Refresh field so filter applies immediately     
    },
    to_rack(frm, cdt, cdn) {
        let count = 0 
        setInterval(() => {
            if (count < 6){
                frm.set_query("to_bin_location", "items", function () {
                    let child = locals[cdt][cdn];
                    return {
                        filters: {
                            rack_name: child.rack
                        },
                    };
                });
                frm.refresh_field('items');
                count++;
            }
        }, 100);
    },
});
