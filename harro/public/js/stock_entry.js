frappe.ui.form.on("Stock Entry", {
    refresh: function (frm) {
       
	},
    items_on_form_rendered(frm){
       
        cur_frm.fields_dict["items"].grid.get_field("bin_location").get_query = function (doc) {
            return {
                query: "harro.harro.docevents.stock_entry.get_bin_location",
                filters: { rack: d.rack },
            };
        };
    }
})

frappe.ui.form.on('Stock Entry Detail', {
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
