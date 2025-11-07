frappe.ui.form.on("Stock Entry", {
    refresh: function (frm) {
       
	},
    items_on_form_rendered(frm){
       
        console.log("hhhhhh")
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
        let row = locals[cdt][cdn];
        // Refresh field so filter applies immediately
        frm.fields_dict['items'].grid.get_field('bin_location').get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                filters: {
                    rack_name: child.rack
                }
            };
        };
        frm.refresh_field('items');
    },
    to_rack(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Refresh field so filter applies immediately
        frm.fields_dict['items'].grid.get_field('to_bin_location').get_query = function(doc, cdt, cdn) {
            let child = locals[cdt][cdn];
            return {
                filters: {
                    rack_name: child.rack
                }
            };
        };
        frm.refresh_field('items');
    },

});
