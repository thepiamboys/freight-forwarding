# -*- coding: utf-8 -*-
"""
Constants for Freight Forwarding App
"""

# Division codes for naming series
DIVISION_CODES = {
    "Export": "EXP",
    "Import": "IMP",
    "Domestic": "DOM",
    "Project": "PRJ",
}

# Mode codes for naming series
MODE_CODES = {
    "Sea": "SEA",
    "Air": "AIR",
    "Land": "LAN",
}

# Service type mapping from Item Group
SERVICE_TYPE_MAP = {
    "Freight": "Freight",
    "Customs": "Customs",
    "Trucking": "Trucking",
    "Port": "Port",
    "Warehouse": "Warehouse",
    "Surcharges": "Surcharges",
}

# Item Group root
ITEM_GROUP_ROOT = "Freight Services"

# Default accounts mapping
DEFAULT_ACCOUNTS = {
    "revenue": {
        "Freight": "Freight Revenue",
        "Customs": "Customs Service Revenue",
        "Trucking": "Trucking Revenue",
        "Port": "Port Service Revenue",
        "Warehouse": "Warehouse Service Revenue",
        "Surcharges": "Surcharges Revenue",
    },
    "direct_cost": {
        "Freight": "Freight Cost",
        "Customs": "Customs Service Cost",
        "Trucking": "Trucking Cost",
        "Port": "Port Service Cost",
        "Warehouse": "Warehouse Service Cost",
        "Surcharges": "Surcharges Cost",
    },
}

# Allowed service types
ALLOWED_SERVICE_TYPES = [
    "Freight",
    "Customs",
    "Trucking",
    "Port",
    "Warehouse",
    "Surcharges",
]

# Allowed divisions
ALLOWED_DIVISIONS = ["Export", "Import", "Domestic", "Project"]

# Allowed modes
ALLOWED_MODES = ["Sea", "Air", "Land"]

