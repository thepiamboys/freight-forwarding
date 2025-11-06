# Testing Guide

## Test Structure

```
freight_forwarding/tests/
├── unit/                    # Unit tests
│   ├── test_naming_series.py
│   ├── test_tax_configuration.py
│   ├── test_expense_claim.py
│   ├── test_advance_line.py
│   └── test_permission_query.py
└── integration/             # Integration tests
    └── test_e2e_workflow.py
```

## Running Tests

### Run All Tests

```bash
bench --site [site-name] run-tests --app freight_forwarding
```

### Run Specific Test File

```bash
bench --site [site-name] run-tests --app freight_forwarding --doctype "Test Naming Series"
```

### Run with Coverage

```bash
bench --site [site-name] run-tests --app freight_forwarding --coverage
```

## Test Coverage Target

- **Minimum**: 60%
- **Target**: 80%

## Writing Tests

### Unit Test Example

```python
import unittest
import frappe
from frappe.tests.utils import FrappeTestCase

class TestMyFeature(FrappeTestCase):
    def setUp(self):
        """Set up test data"""
        pass
    
    def test_feature(self):
        """Test description"""
        # Test implementation
        pass
```

### Integration Test Example

```python
class TestWorkflow(FrappeTestCase):
    def test_complete_workflow(self):
        """Test end-to-end workflow"""
        # Create documents
        # Verify results
        pass
```

## Test Checklist

- [ ] Naming series tests
- [ ] Tax configuration tests
- [ ] Expense claim consumption tests
- [ ] Advance line balance tests
- [ ] PQC filtering tests
- [ ] E2E workflow tests
- [ ] Coverage ≥ 60%

## Notes

- Tests require Frappe environment to be running
- Use `FrappeTestCase` as base class
- Set up test data in `setUp()` method
- Clean up test data in `tearDown()` if needed

