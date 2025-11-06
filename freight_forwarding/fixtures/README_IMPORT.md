# Data Import Guide

## FF Port Import

### CSV Template
File: `port_template.csv`

### Columns
- `port_code` (required, unique) - Port code (e.g., IDJKT)
- `port_name` (required) - Port name
- `country` (required) - Country name (must exist in Country master)
- `city` - City name
- `port_type` - Sea/River/Rail/ICD
- `lat` - Latitude (optional)
- `lon` - Longitude (optional)
- `timezone` - Timezone (optional)
- `has_customs` - 1/0 or true/false
- `free_time_default_demurrage` - Days (optional)
- `free_time_default_detention` - Days (optional)

### Import Methods

#### Method 1: Via API (after app installed)
```python
import frappe
from freight_forwarding.utils.import_data import import_ports_bootstrap

result = import_ports_bootstrap()
print(result)
```

#### Method 2: Via Bench Console
```bash
bench --site [site] console
```

Then in console:
```python
from freight_forwarding.utils.import_data import import_ports_bootstrap
result = import_ports_bootstrap()
print(result)
```

#### Method 3: Via Frappe Data Import
1. Go to Setup → Data → Data Import
2. Select DocType: FF Port
3. Upload CSV file
4. Map columns and import

## FF Airport Import

### CSV Template
File: `airport_template.csv`

### Columns
- `iata` (required, unique) - IATA code (e.g., CGK)
- `icao` (optional) - ICAO code
- `airport_name` (required) - Airport name
- `city` - City name
- `country` (required) - Country name (must exist in Country master)
- `lat` - Latitude (optional)
- `lon` - Longitude (optional)
- `timezone` - Timezone (optional)
- `has_customs` - 1/0 or true/false

### Import Methods
Same as FF Port import methods above, but use:
- `import_airports_bootstrap()` function
- DocType: FF Airport

## Bootstrap Data

The template files (`port_template.csv` and `airport_template.csv`) contain common ports and airports in Asia-Pacific region. You can extend these files with additional data as needed.

## Notes

1. **Country Master**: Ensure all countries referenced in CSV exist in ERPNext Country master before importing.
2. **Duplicate Check**: Import scripts automatically skip existing records based on port_code/iata.
3. **Validation**: All data is validated according to FF Port/FF Airport doctype validations.
4. **Coordinates**: Latitude/Longitude are optional but recommended for accurate location tracking.

