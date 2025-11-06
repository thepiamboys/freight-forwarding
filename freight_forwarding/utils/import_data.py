# -*- coding: utf-8 -*-
"""
Data Import Utilities for FF Port and FF Airport
"""

import frappe
import csv
import os
from frappe import _


def import_ports_from_csv(file_path):
    """
    Import FF Port data from CSV file.
    
    Args:
        file_path: Path to CSV file
    
    Returns:
        dict: Summary of import results
    """
    if not os.path.exists(file_path):
        frappe.throw(_("File not found: {0}").format(file_path))

    imported = 0
    skipped = 0
    errors = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                port_code = row.get("port_code", "").strip().upper()
                if not port_code:
                    skipped += 1
                    continue

                # Check if port already exists
                if frappe.db.exists("FF Port", port_code):
                    skipped += 1
                    continue

                # Create new port
                port = frappe.get_doc({
                    "doctype": "FF Port",
                    "port_code": port_code,
                    "port_name": row.get("port_name", "").strip(),
                    "country": row.get("country", "").strip(),
                    "city": row.get("city", "").strip(),
                    "port_type": row.get("port_type", "Sea").strip(),
                    "lat": float(row.get("lat", 0)) if row.get("lat") else None,
                    "lon": float(row.get("lon", 0)) if row.get("lon") else None,
                    "timezone": row.get("timezone", "").strip(),
                    "has_customs": bool(row.get("has_customs", "").lower() in ["1", "true", "yes"]),
                    "free_time_default_demurrage": int(row.get("free_time_default_demurrage", 0)) if row.get("free_time_default_demurrage") else None,
                    "free_time_default_detention": int(row.get("free_time_default_detention", 0)) if row.get("free_time_default_detention") else None,
                })
                port.insert()
                imported += 1

            except Exception as e:
                errors.append(f"Row {port_code}: {str(e)}")

    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
    }


def import_airports_from_csv(file_path):
    """
    Import FF Airport data from CSV file.
    
    Args:
        file_path: Path to CSV file
    
    Returns:
        dict: Summary of import results
    """
    if not os.path.exists(file_path):
        frappe.throw(_("File not found: {0}").format(file_path))

    imported = 0
    skipped = 0
    errors = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                iata = row.get("iata", "").strip().upper()
                if not iata:
                    skipped += 1
                    continue

                # Check if airport already exists
                if frappe.db.exists("FF Airport", iata):
                    skipped += 1
                    continue

                # Create new airport
                airport = frappe.get_doc({
                    "doctype": "FF Airport",
                    "iata": iata,
                    "icao": row.get("icao", "").strip().upper() if row.get("icao") else None,
                    "airport_name": row.get("airport_name", "").strip(),
                    "city": row.get("city", "").strip(),
                    "country": row.get("country", "").strip(),
                    "lat": float(row.get("lat", 0)) if row.get("lat") else None,
                    "lon": float(row.get("lon", 0)) if row.get("lon") else None,
                    "timezone": row.get("timezone", "").strip(),
                    "has_customs": bool(row.get("has_customs", "").lower() in ["1", "true", "yes"]),
                })
                airport.insert()
                imported += 1

            except Exception as e:
                errors.append(f"Row {iata}: {str(e)}")

    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
    }


@frappe.whitelist()
def import_ports_bootstrap():
    """
    Import bootstrap FF Port data from fixtures.
    """
    file_path = os.path.join(
        frappe.get_app_path("freight_forwarding"),
        "fixtures",
        "port_template.csv"
    )
    return import_ports_from_csv(file_path)


@frappe.whitelist()
def import_airports_bootstrap():
    """
    Import bootstrap FF Airport data from fixtures.
    """
    file_path = os.path.join(
        frappe.get_app_path("freight_forwarding"),
        "fixtures",
        "airport_template.csv"
    )
    return import_airports_from_csv(file_path)

