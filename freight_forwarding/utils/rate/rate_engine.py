# -*- coding: utf-8 -*-
"""
Rate Engine for Freight Forwarding

Filter active + within validity by lane
Calculate total buy = base + surcharges ± fuel index/FX
Apply pricing rule → sell
Return ranked options (cost, transit, carrier)
"""

import frappe
from frappe import _
from datetime import date


def find_rates(lane_type, origin, destination, mode, date_filter=None, weight=None, cbm=None, container_type=None):
    """
    Find rates for a given lane.
    
    Args:
        lane_type: "Sea", "Air", or "Land"
        origin: POL (for Sea), AOO (for Air), or origin city (for Land)
        destination: POD (for Sea), AOD (for Air), or destination city (for Land)
        mode: "Sea", "Air", or "Land"
        date_filter: Date to check validity (default: today)
        weight: Weight in kg (optional)
        cbm: Volume in CBM (optional)
        container_type: Container type for Sea (optional)
    
    Returns:
        list: Ranked rate options with buy/sell prices
    """
    if not date_filter:
        date_filter = date.today()
    
    # Find active rate contracts
    rate_contracts = frappe.get_all(
        "FF Rate Contract",
        filters={
            "status": "Active",
            "mode": ["like", f"%{mode}%"],
            "validity_from": ["<=", date_filter],
            "validity_to": [">=", date_filter],
        },
        fields=["name", "vendor", "carrier", "currency", "mode"]
    )
    
    if not rate_contracts:
        return []
    
    options = []
    
    for contract in rate_contracts:
        contract_doc = frappe.get_doc("FF Rate Contract", contract.name)
        
        # Find matching lanes
        matching_lanes = find_matching_lanes(
            contract_doc, lane_type, origin, destination, mode
        )
        
        for lane in matching_lanes:
            # Calculate buy rate
            buy_rate = calculate_buy_rate(contract_doc, lane, weight, cbm, container_type)
            
            if buy_rate:
                # Apply pricing rules to get sell rate
                sell_rate = apply_pricing_rules(
                    buy_rate, contract_doc, lane, mode
                )
                
                options.append({
                    "rate_contract": contract.name,
                    "vendor": contract.vendor,
                    "carrier": contract.carrier or contract.vendor,
                    "lane": lane.name if hasattr(lane, 'name') else None,
                    "transit_days": lane.transit if hasattr(lane, 'transit') else None,
                    "buy_rate": buy_rate,
                    "sell_rate": sell_rate,
                    "currency": contract.currency,
                    "margin": sell_rate - buy_rate if sell_rate and buy_rate else None,
                    "margin_percent": ((sell_rate - buy_rate) / buy_rate * 100) if sell_rate and buy_rate and buy_rate > 0 else None,
                })
    
    # Rank options by cost (buy_rate), then by transit
    options.sort(key=lambda x: (x.get("buy_rate") or float('inf'), x.get("transit_days") or float('inf')))
    
    return options


def find_matching_lanes(contract_doc, lane_type, origin, destination, mode):
    """Find matching lanes in rate contract"""
    matching_lanes = []
    
    for lane in contract_doc.rate_lanes:
        if lane.lane_type != lane_type:
            continue
        
        if mode == "Sea":
            if lane.pol == origin and lane.pod == destination:
                matching_lanes.append(lane)
        elif mode == "Air":
            if lane.aoo == origin and lane.aod == destination:
                matching_lanes.append(lane)
        elif mode == "Land":
            if lane.origin == origin and lane.destination == destination:
                matching_lanes.append(lane)
    
    return matching_lanes


def calculate_buy_rate(contract_doc, lane, weight=None, cbm=None, container_type=None):
    """
    Calculate buy rate = base + surcharges ± fuel index/FX
    
    Args:
        contract_doc: FF Rate Contract document
        lane: FF Rate Lane document
        weight: Weight in kg
        cbm: Volume in CBM
        container_type: Container type
    
    Returns:
        float: Total buy rate
    """
    # Get base rate
    base_rate = get_base_rate(contract_doc, lane, weight, cbm, container_type)
    
    if not base_rate:
        return None
    
    # Get surcharges
    surcharges_total = calculate_surcharges(contract_doc, lane, weight, cbm, container_type)
    
    # TODO: Apply fuel index/FX adjustments
    # fuel_adjustment = get_fuel_index_adjustment(contract_doc, lane)
    # fx_adjustment = get_fx_adjustment(contract_doc)
    
    total_buy = base_rate + surcharges_total
    
    return total_buy


def get_base_rate(contract_doc, lane, weight=None, cbm=None, container_type=None):
    """Get base rate from rate bases"""
    if not contract_doc.rate_bases:
        return 0
    
    # Find matching rate base
    for rate_base in contract_doc.rate_bases:
        if rate_base.rate_lane != lane.name:
            continue
        
        # Match by container type (Sea)
        if container_type and rate_base.container_type:
            if rate_base.container_type == container_type:
                return float(rate_base.base_rate or 0)
        
        # Match by weight break
        if weight and rate_base.weight_break_from and rate_base.weight_break_to:
            if rate_base.weight_break_from <= weight <= rate_base.weight_break_to:
                return float(rate_base.base_rate or 0)
    
    # If no match, return first base rate or 0
    if contract_doc.rate_bases:
        return float(contract_doc.rate_bases[0].base_rate or 0)
    
    return 0


def calculate_surcharges(contract_doc, lane, weight=None, cbm=None, container_type=None):
    """Calculate total surcharges"""
    if not contract_doc.rate_surcharges:
        return 0
    
    total_surcharges = 0
    
    for surcharge in contract_doc.rate_surcharges:
        amount = float(surcharge.amount or 0)
        calc_type = surcharge.calc_type
        
        if calc_type == "flat":
            total_surcharges += amount
        elif calc_type == "per_kg" and weight:
            total_surcharges += amount * weight
        elif calc_type == "per_cntr" and container_type:
            total_surcharges += amount
        elif calc_type == "percent":
            # Percent of base rate (would need base rate here)
            # For simplicity, using flat amount
            total_surcharges += amount
    
    return total_surcharges


def apply_pricing_rules(buy_rate, contract_doc, lane, mode):
    """
    Apply pricing rules to calculate sell rate.
    
    Args:
        buy_rate: Buy rate
        contract_doc: FF Rate Contract document
        lane: FF Rate Lane document
        mode: Mode (Sea/Air/Land)
    
    Returns:
        float: Sell rate
    """
    if not buy_rate:
        return None
    
    # Find applicable pricing rules
    pricing_rules = frappe.get_all(
        "FF Pricing Rule",
        filters={
            "status": "Active",
            "mode": ["like", f"%{mode}%"],
        },
        fields=["name", "priority", "markup_type", "markup_value", "discount_type", "discount_value"],
        order_by="priority asc"
    )
    
    sell_rate = buy_rate
    
    # Apply first matching pricing rule
    for rule_doc in pricing_rules:
        rule = frappe.get_doc("FF Pricing Rule", rule_doc.name)
        
        # Check if rule matches (division, customer, commodity, validity)
        # For now, apply first rule found
        if rule.markup_value:
            if rule.markup_type == "Percentage":
                sell_rate = sell_rate * (1 + rule.markup_value / 100)
            else:
                sell_rate = sell_rate + rule.markup_value
        
        if rule.discount_value:
            if rule.discount_type == "Percentage":
                sell_rate = sell_rate * (1 - rule.discount_value / 100)
            else:
                sell_rate = sell_rate - rule.discount_value
        
        # Apply only first matching rule
        break
    
    return sell_rate

