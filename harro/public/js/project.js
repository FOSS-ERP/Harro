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

        loadChartJS(() => renderAllSpeedometers(frm));
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
    const percentage = planned ? Math.min((actual / planned) * 100, 150) : 0;

    const ctx = document.getElementById(`speed_chart_${index}_${frm.doc.name}`);
    if (!ctx) return;

    // Color zones
    const actualColor =
        percentage < 100 ? "#1abc9c" :
        percentage <= 150 ? "#f1c40f" :
        "#e74c3c";
    console.log(percentage)
    // Planned arc (green→yellow→red) + Actual overlay
    const data = {
        datasets: [
            {
                // Planned zones
                data: [50, 25, 25],
                backgroundColor: ["#2ecc71", "#ffe733", "#e74c3c"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "75%",
            },
            {
                // Actual arc
                data: [percentage, Math.abs(200 - percentage)],
                backgroundColor: [actualColor, "rgba(0,0,0,0)"],
                borderWidth: 0,
                circumference: 180,
                rotation: 270,
                cutout: "75%",
            }
        ]
    };

    const options = {
        responsive: false,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
        },
    };

    // Prevent duplicate charts
    if (frm[`_speed_chart_${index}`]) frm[`_speed_chart_${index}`].destroy();

    frm[`_speed_chart_${index}`] = new Chart(ctx, {
        type: "doughnut",
        data: data,
        options: options
    });

    document.getElementById(`speed_value_${index}_${frm.doc.name}`).innerHTML =
        `${percentage.toFixed(1)}%<br>(${actual || 0} / ${planned || 0} hrs)`;
}
