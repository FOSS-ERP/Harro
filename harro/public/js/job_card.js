frappe.ui.form.on("Job Card", {
    complete_job: function (frm, status, completed_qty) {
        if(status == 'On Hold'){
            let d = new frappe.ui.Dialog({
            title: 'Update Unproductive Activity',
            fields: [
                {
                    "fieldname" : "activity_type",
                    "label" : "Activity Type",
                    "options" : "Activity Type",
                    "reqd" :  1,
                    "fieldtype" : "Link"
                },
                {
                    "fieldname" : "project",
                    "label" : "BA Number",
                    "options" : "Project",
                    "reqd" :  1,
                    "fieldtype" : "Link",
                    "default" : frm.doc.name
                },
                {
                    "fieldname" : "task",
                    "label" : "Task",
                    "options" : "Task",
                    "reqd" :  0,
                    "fieldtype" : "Link"
                },
                {
                    "fieldname" : "expected_hrs",
                    "label" : "Expected Hrs",
                    "reqd" :  0,
                    "fieldtype" : "Float"
                }
            ],
            size: 'small', // small, large, extra-large 
            primary_action_label: 'Submit',
            primary_action(values) {
                console.log(values);
                d.hide();
            }
        });
        d.show();
        }else{
            const args = {
                job_card_id: frm.doc.name,
                complete_time: frappe.datetime.now_datetime(),
                status: status,
                completed_qty: completed_qty,
            };
            frm.events.make_time_log(frm, args);
        }
	},
})