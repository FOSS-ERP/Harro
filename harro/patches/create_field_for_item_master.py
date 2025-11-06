import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    # Create Tab Break first
    frappe.get_doc({
        "is_system_generated": 1,
        "module": "Harro",
        "doctype": "Custom Field",
        "dt": "Item",
        "fieldname": "bom_sheet_details",
        "insert_after": "serial_no_series",
        "label": "BOM Sheet Details",
        "fieldtype": "Tab Break"
    }).insert(ignore_if_duplicate=True)

    # Labels list
    labels = [
        "Baugruppe",
        "Baugruppe HH_India",
        "StrukturklasseKopf",
        "Revision",
        "Revision alt",
        "Position",
        "Position alt",
        "Artikel",
        "Artikel HH_India",
        "StrukturklassePos",
        "Revision Artikel",
        "Artikel alt",
        "Artikel alt HH_India",
        "StrukturklassePos alt",
        "Revision Artikel alt",
        "Menge",
        "Mengeneinheit",
        "Menge alt",
        "Mengeneinheit alt",
        "initial",
        "status",
        "cHerstellernr",
        "cHerstellerBez",
        "cHerstellerBez2",
        "cHerstellerBez3",
        "cHerstellerBez4",
        "cBestellnummer",
        "iLieferant",
        "cLieferantSuchbegriff",
        "cLiefBez",
        "cLiefBez2",
        "cLiefBez3",
        "cLiefBez4",
        "cLiefBestellnummer",
        "Baugruppe Bez1",
        "Baugruppe Bez2",
        "Baugruppe Bez3",
        "Baugruppe Bez4",
        "Baugruppe pruefplan",
        "Baugruppe Werkstoff",
        "Baugruppe Oberflaechenbehandlung",
        "Baugruppe Rohteil",
        "Baugruppe Schweissteil",
        "Baugruppe Halbzeug",
        "Artikel Bez1",
        "Artikel Bez2",
        "Artikel Bez3",
        "Artikel Bez4",
        "Artikel pruefplan",
        "Artikel Werkstoff",
        "Artikel Oberflaechenbehandlung",
        "Artikel Rohteil",
        "Artikel Schweissteil",
        "Artikel Halbzeug",
        "Stufe Baugruppenpos",
        "HerstellerNr HH_India",
        "sequenz",
        "Anzahl",
        "Menge Brutto",
        "Gesamtmenge"
    ]

    # Helper: make snake_case fieldname
    def make_fieldname(label):
        return label.strip().lower().replace(" ", "_")

    custom_fields = []
    total = len(labels)
    half = total // 2
    count = 0
    last_fieldname = "bom_sheet_details"  # Start after tab break

    for label in labels:
        fieldname = make_fieldname(label)
        field = {
            "fieldname": fieldname,
            "label": label,
            "fieldtype": "Data",
            "insert_after": last_fieldname
        }
        custom_fields.append(field)
        last_fieldname = fieldname
        count += 1

        # Add column break at halfway point
        if count == half:
            column_break_name = f"column_break_1"
            custom_fields.append({
                "fieldname": column_break_name,
                "fieldtype": "Column Break",
                "insert_after": last_fieldname
            })
            last_fieldname = column_break_name  # update for next field

    create_custom_fields({
        "Item": custom_fields
    })

    print(f"✅ Created {len(labels)} BOM Sheet fields in Item doctype with column break.")
