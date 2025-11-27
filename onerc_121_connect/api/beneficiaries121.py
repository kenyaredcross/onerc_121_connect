import frappe
import requests

@frappe.whitelist()
def get_121_contacts(program_id, page=1, limit=20, token=None):

    try:
        BASE_URL = "https://krcs.121.global/api/programs"
        URL = f"{BASE_URL}/{program_id}/registrations"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",

        }

        params = {
            "page": page,
            "limit": limit
        }


        response = requests.get(URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        cleaned = []
        for row in data.get("data", []):
            cleaned.append({
                "reference_id": row.get("referenceId"),
                "name": row.get("data", {}).get("value", {}).get("fullName"),
                "project": row.get("registrationProgramId"),
                "phone": row.get("phoneNumber"),
            })

        return cleaned


    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "get 121 Contacts")
        frappe.throw(f"Failed to get: {e}")



def sync_121_contacts(program_id, token, page=1, limit=50):

    records = get_121_contacts(program_id, page, limit, token)

    inserted = []

    for r in records:
        if not r.get("phone"):
            continue

        doc = frappe.get_doc({
            "doctype": "Red Profile", 
            "full_name": r["name"],
            "project": r.get("project"),
            "phone_number": r.get("phone"),
            "reference_id": r.get("reference_id")
        })


        doc.insert(ignore_permissions=True)
        inserted.append(doc.name)

        return {
            "message": f"Inserted {len(inserted)} recipients",
            "records": inserted
        }
