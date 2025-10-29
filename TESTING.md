# Testing Guide

This document provides information about the test suite for the Tree Management API.

## Overview

The project includes comprehensive unit tests covering:
- API endpoints (tree and model operations)
- Data models and schemas
- Query builder functionality
- Service layer logic

## Running Tests

### Run All Tests
```bash
pytest tests/
```

### Run with Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/services/test_query_builder.py
```

### Run Specific Test Class
```bash
pytest tests/api/test_tree.py::TestTreeAPI
```

### Run Specific Test
```bash
pytest tests/api/test_tree.py::TestTreeAPI::test_create_tree
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── api/
│   ├── test_tree.py        # Tree API endpoint tests
│   └── test_model.py       # Model API endpoint tests
├── models/
│   └── test_schemas.py     # Pydantic model tests
└── services/
    └── test_query_builder.py  # Query builder tests
```

## Coverage

Current test coverage: **64%**

Coverage by module:
- Query Builder: **100%**
- Models/Schemas: **100%**
- Config: **100%**
- API Endpoints: **77-89%**
- Services: **17-40%** (mocked in integration tests)

View detailed coverage report:
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

## Test Fixtures

### Common Fixtures (conftest.py)

- `mock_es_client`: Mocked Elasticsearch client
- `sample_tree_node`: Sample tree node data
- `sample_tree_node_with_parent`: Tree node with parent relation

### API Test Fixtures

- `client`: FastAPI test client with mocked Elasticsearch

## Writing New Tests

### API Endpoint Tests

```python
def test_my_endpoint(self, client):
    """Test my new endpoint"""
    with patch("app.api.tree.tree_service") as mock_service:
        mock_service.my_method.return_value = expected_result
        
        response = client.post("/api/my-endpoint", json={...})
        
        assert response.status_code == 200
        assert response.json()["code"] == 0
```

### Model Tests

```python
def test_my_model(self):
    """Test my model validation"""
    model = MyModel(field1="value1", field2="value2")
    assert model.field1 == "value1"
```

### Query Builder Tests

```python
def test_my_query(self):
    """Test my query builder"""
    query = MyQueryBuilder.build_query(...)
    assert "query" in query
    # Assert query structure
```

## Code Quality Tools

### Black (Code Formatting)
```bash
# Check formatting
black --check app/ tests/ main.py

# Auto-format
black app/ tests/ main.py
```

### isort (Import Sorting)
```bash
# Check imports
isort --check app/ tests/ main.py

# Auto-sort
isort app/ tests/ main.py
```

### Flake8 (Linting)
```bash
flake8 app/ tests/ main.py
```

### Run All Quality Checks
```bash
black app/ tests/ main.py && \
isort app/ tests/ main.py && \
flake8 app/ tests/ main.py && \
pytest tests/ --cov=app
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines. Key features:
- Fast execution (< 10 seconds)
- No external dependencies (mocked Elasticsearch)
- Comprehensive coverage
- Clear failure messages

## Best Practices

1. **Mock External Dependencies**: Always mock Elasticsearch and other external services
2. **Test One Thing**: Each test should verify one specific behavior
3. **Use Descriptive Names**: Test names should clearly describe what they test
4. **Follow AAA Pattern**: Arrange, Act, Assert
5. **Keep Tests Independent**: Tests should not depend on each other
6. **Use Fixtures**: Reuse common test data and setup
7. **Test Error Cases**: Include tests for error handling
8. **Maintain Coverage**: Aim for >80% code coverage

## Troubleshooting

### Import Errors
If you get import errors, ensure you're running tests from the project root:
```bash
cd /path/to/copilot-todo-list-demo
pytest tests/
```

### Elasticsearch Connection Errors
Tests should NOT connect to real Elasticsearch. If you see connection errors:
1. Check that mocks are properly configured
2. Ensure fixtures are being used
3. Verify patch decorators are at the correct level

### Coverage Issues
To see which lines are not covered:
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

## Future Improvements

- [ ] Add integration tests with real Elasticsearch (optional)
- [ ] Add performance benchmarks
- [ ] Add API contract tests
- [ ] Increase service layer test coverage
- [ ] Add mutation testing
- [ ] Add property-based testing

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/)
