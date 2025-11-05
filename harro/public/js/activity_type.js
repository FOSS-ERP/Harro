frappe.ui.form.on("Project", {
    refresh:function(frm){
        if(!frappe.user.has_role("System Manager")){
            frm.set_db_property("Activity Type", "hidden", 1)
        }
    }
})