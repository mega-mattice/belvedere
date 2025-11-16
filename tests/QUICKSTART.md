# Pytest Quick Reference for Belvedere

## Common Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/test_config.py

# Run specific test
pytest tests/test_config.py::TestFolderManagement::test_add_folder_succeeds

# Run tests matching pattern
pytest -k "add_folder"

# Run with coverage
pytest --cov=belvedere --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=belvedere --cov-report=html

# Run tests by marker
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Show print statements
pytest -s

# Stop at first failure
pytest -x

# Run last failed tests
pytest --lf

# Show test durations
pytest --durations=10
```

## Key Features

- ✅ 85 comprehensive tests
- ✅ 97% coverage on config.py
- ✅ 82% coverage on rule_engine.py
- ✅ 89% coverage on file_monitor.py
- ✅ Organized test classes
- ✅ Shared fixtures in conftest.py
- ✅ Parametrized tests
- ✅ Mocked external dependencies
- ✅ Test markers for categorization
- ✅ AAA pattern (Arrange, Act, Assert)
