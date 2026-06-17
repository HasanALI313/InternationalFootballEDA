# Tests Directory

## Overview
This directory contains unit tests and integration tests for the International Football EDA project.

## Test Structure

```
tests/
├── README.md              # This file
├── test_sample.py         # Sample test file (replace with real tests)
├── test_bronze.py         # Tests for Bronze layer (to be created)
├── test_silver.py         # Tests for Silver layer (to be created)
├── test_gold.py           # Tests for Gold layer (to be created)
├── test_ml_model.py       # Tests for ML models (to be created)
└── test_simulation.py     # Tests for World Cup simulation (to be created)
```

## Running Tests

### Locally
```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_sample.py -v

# Run specific test class
pytest tests/test_sample.py::TestDataQuality -v

# Run specific test method
pytest tests/test_sample.py::TestDataQuality::test_catalog_name_format -v
```

### In CI/CD
Tests run automatically on:
* Pull requests (all tests)
* Pushes to develop branch (all tests)
* Manual workflow dispatch

## Test Types

### Unit Tests
Test individual functions and components in isolation.

**Examples:**
* Data transformation functions
* Validation logic
* Utility functions
* Schema validations

### Integration Tests
Test workflows end-to-end in a Databricks environment.

**Examples:**
* Bronze layer ingestion
* Silver layer transformations
* Gold layer aggregations
* ML model training
* Full pipeline execution

## Writing Tests

### Test Naming Convention
* Test files: `test_<module_name>.py`
* Test classes: `Test<Feature>`
* Test methods: `test_<what_is_being_tested>`

### Example Test Structure
```python
import pytest

class TestBronzeLayer:
    \"\"\"Tests for Bronze layer data ingestion.\"\"\"
    
    def test_data_ingestion(self):
        \"\"\"Test that raw data is ingested correctly.\"\"\"
        # Arrange
        expected_columns = ["team", "date", "score"]
        
        # Act
        # result = ingest_data()
        
        # Assert
        # assert set(result.columns) == set(expected_columns)
        pass
    
    def test_schema_validation(self):
        \"\"\"Test that ingested data has correct schema.\"\"\"
        pass
```

## Test Data

Store test fixtures and sample data in:
* `tests/fixtures/` - Small test data files
* `tests/data/` - Larger test datasets (git-ignored)

## Coverage Goals

Aim for:
* **80%+ code coverage** for utility functions
* **60%+ coverage** for data pipelines
* **90%+ coverage** for business logic

## Continuous Improvement

As you develop:
1. Write tests for new features
2. Add tests when fixing bugs
3. Update tests when requirements change
4. Review coverage reports regularly

## Resources

* [pytest documentation](https://docs.pytest.org/)
* [pytest-cov plugin](https://pytest-cov.readthedocs.io/)
* [Testing PySpark applications](https://docs.databricks.com/dev-tools/testing.html)
