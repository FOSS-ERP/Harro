frappe.ui.form.on("Project", {
    refresh:function(frm){
        if(!frappe.user.has_role("System Manager")){
            frm.set_db_property("custom_update_to_project_field", "hidden", 1)
            frm.set_db_property("custom_planned_hours_field_name", "hidden", 1)
        }
    }
})