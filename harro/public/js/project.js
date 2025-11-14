frappe.ui.form.on("Project", {
    refresh(frm) {
        if (!frm.fields_dict.effort_overview) return;

        const wrapper = frm.fields_dict.effort_overview.$wrapper;

        // Add chart containers if not already added
        if (!wrapper.find(".multi-effort-wrapper").length) {
            wrapper.html(`
                <div class="multi-effort-wrapper" style="display:flex; justify-content:space-around; flex-wrap:wrap; gap:20px;">
                    ${["Effort Construction", "Effort Mechanical", "Effort Electrical"].map((title, i) => `
                        <div class="effort-chart-wrapper" 
                             style="width:300px; margin:0 auto; text-align:center; position:relative;">
                            <h5 style="font-weight:600; margin-bottom:4px;">${title}</h5>
                            <canvas id="speed_chart_${i}_${frm.doc.name}" width="300" height="180"
                                    style="display:block; margin:0 auto;"></canvas>
                            <div id="speed_value_${i}_${frm.doc.name}" 
                                 style="position:absolute; top:58%; left:50%; transform:translate(-50%, -50%);
                                        font-weight:600; font-size:14px;">
                            </div>
                        </div>
                    `).join('')}
                </div>
            `);
        }

        let acivity_type = []
        frappe.call({
            method : "harro.harro.docevents.project.get_activity",
            args:{

            },
            callback:function(r){
                acivity_type = r.message
            }
        })
        const t_wrapper = frm.fields_dict.custom_timesheet_chart.$wrapper;
        if (!t_wrapper.find(".multi-effort-wrapper").length) {
            frappe.call({
            method : "harro.harro.docevents.project.get_activity",
            args:{

            },
            callback:function(r){
                acivity_type = r.message
            
            t_wrapper.html(`
                <div class="multi-effort-wrapper" style="display:flex; justify-content:space-around; flex-wrap:wrap; gap:20px;">
                    ${acivity_type.map((title, i) => `
                        <div class="effort-chart-wrapper" 
                             style="width:300px; margin:0 auto; text-align:center; position:relative;">
                            <h5 style="font-weight:600; margin-bottom:4px;">${title}</h5>
                            <canvas id="timesheet_chart_${i}_${frm.doc.name}" width="300" height="180"
                                    style="display:block; margin:0 auto;"></canvas>
                            <div id="timesheet_value_${i}_${frm.doc.name}" 
                                 style="position:absolute; top:58%; left:50%; transform:translate(-50%, -50%);
                                        font-weight:600; font-size:14px;">
                            </div>
                        </div>
                    `).join('')}
                </div>
            `);
            }
        })
        }
        loadChartJS(() => {
            renderAllSpeedometers(frm);
            renderAllTimesheetSpeedometers(frm);
        });
    }
});

function loadChartJS(callback) {
    if (window.Chart) {
        callback();
        return;
    }
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/chart.js";
    script.onload = callback;
    document.head.appendChild(script);
}

function renderAllSpeedometers(frm) {
    frappe.call({
        method: "harro.harro.docevents.project.get_effort_data",
        args: { project: frm.doc.name },
        callback: function (r) {
            if (!r.message) return;

            const dataSets = [
                {
                    label: "Manufacturing Hours",
                    planned: r.message.planned_manufacturing_hours,
                    actual: r.message.actual_manufacturing_hours,
                    index: 0
                },
                {
                    label: "Mechanical Assembly",
                    planned: r.message.planned_mechanical_assembly,
                    actual: r.message.actual_mechanical_assembly,
                    index: 1
                },
                {
                    label: "Electrical Assembly",
                    planned: r.message.planned_electrical_assembly,
                    actual: r.message.actual_electrical_assembly,
                    index: 2
                }
            ];

            dataSets.forEach(set => renderSpeedometer(frm, set));
        }
    });
}

function renderSpeedometer(frm, set) {
    const { planned, actual, index } = set;
    const percentage = planned ? Math.min((actual / planned) * 100, 200) : 0;

    const ctx = document.getElementById(`speed_chart_${index}_${frm.doc.name}`);
    if (!ctx) return;

    let actualColor;
    if (percentage < 80) actualColor = "#2ecc71"; // Green
    else if (percentage < 90) actualColor = "#f1c40f"; // Yellow
    else if (percentage <= 100) actualColor = "#FFA500"; // Orange
    else actualColor = "#e74c3c"; // Red

    const data = {
        datasets: [
            {
                data: [40, 5, 5, 50],
                backgroundColor: ["#2ecc71", "#f1c40f", "#FFA500", "#e74c3c"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "70%",
            },
            {
                data: [percentage, 200 - percentage],
                backgroundColor: [actualColor, "rgba(0,0,0,0)"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "70%",
            },
        ],
    };

    const options = {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
            needle: {
                radiusPercentage: 1.2,
                widthPercentage: 3,
                lengthPercentage: 80,
                color: "#000",
            },
        },
    };

    // Destroy old chart
    if (frm[`_speed_chart_${index}`]) frm[`_speed_chart_${index}`].destroy();

    // Custom Needle Plugin
    const gaugeNeedle = {
        id: "needle",
        afterDatasetDraw(chart) {
            const { ctx, chartArea: { width, height, top } } = chart;
            const needleValue = percentage > 200 ? 200 : percentage;
            const angle = (Math.PI * (needleValue / 200)) - Math.PI; // 0-200 mapped to 180°
            const cx = width / 2;
            const cy = height - 10;

            const length = height * 0.65;
            const needleX = cx + length * Math.cos(angle);
            const needleY = cy + length * Math.sin(angle);

            // Draw needle
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(needleX, needleY);
            ctx.lineWidth = 3;
            ctx.strokeStyle = "#111";
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
            ctx.fillStyle = "#111";
            ctx.fill();
            ctx.restore();
        },
    };

    frm[`_speed_chart_${index}`] = new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: options,
        plugins: [gaugeNeedle],
    });

    // Value label
    document.getElementById(`speed_value_${index}_${frm.doc.name}`).innerHTML =
        `<b>${percentage.toFixed(1)}%</b><br>(${actual || 0} / ${planned || 0} hrs)`;
}



function renderAllTimesheetSpeedometers(frm) {
    frappe.call({
        method: "harro.harro.docevents.project.get_timesheet_working_hours",
        args: { name: frm.doc.name },
        callback: function (r) {
            if (!r.message) return;
            const dataSets = r.message

            dataSets.forEach(set => renderTimesheetSpeedometer(frm, set));
        }
    });
}

function renderTimesheetSpeedometer(frm, set) {
    const { planned, actual, index } = set;
    const percentage = planned ? Math.min((actual / planned) * 100, 200) : 0;

    const ctx = document.getElementById(`timesheet_chart_${index}_${frm.doc.name}`);
    if (!ctx) return;

    let actualColor;
    if (percentage < 80) actualColor = "#2ecc71"; // Green
    else if (percentage < 90) actualColor = "#f1c40f"; // Yellow
    else if (percentage <= 100) actualColor = "#FFA500"; // Orange
    else actualColor = "#e74c3c"; // Red

    const data = {
        datasets: [
            {
                data: [40, 5, 5, 50],
                backgroundColor: ["#2ecc71", "#f1c40f", "#FFA500", "#e74c3c"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "70%",
            },
            {
                data: [percentage, 200 - percentage],
                backgroundColor: [actualColor, "rgba(0,0,0,0)"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "70%",
            },
        ],
    };

    const options = {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
            needle: {
                radiusPercentage: 1.2,
                widthPercentage: 3,
                lengthPercentage: 80,
                color: "#000",
            },
        },
    };

    // Destroy old chart
    if (frm[`_timesheet_chart_${index}`]) frm[`_timesheet_chart_${index}`].destroy();

    // Custom Needle Plugin
    const gaugeNeedle = {
        id: "needle",
        afterDatasetDraw(chart) {
            const { ctx, chartArea: { width, height, top } } = chart;
            const needleValue = percentage > 200 ? 200 : percentage;
            const angle = (Math.PI * (needleValue / 200)) - Math.PI; // 0-200 mapped to 180°
            const cx = width / 2;
            const cy = height - 10;

            const length = height * 0.65;
            const needleX = cx + length * Math.cos(angle);
            const needleY = cy + length * Math.sin(angle);

            // Draw needle
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(needleX, needleY);
            ctx.lineWidth = 3;
            ctx.strokeStyle = "#111";
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
            ctx.fillStyle = "#111";
            ctx.fill();
            ctx.restore();
        },
    };

    frm[`_timesheet_chart_${index}`] = new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: options,
        plugins: [gaugeNeedle],
    });

    // Value label
    document.getElementById(`timesheet_value_${index}_${frm.doc.name}`).innerHTML =
        `<b>${percentage.toFixed(1)}%</b><br>(${actual || 0} / ${planned || 0} hrs)`;
}