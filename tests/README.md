# Belvedere Test Suite

This directory contains the comprehensive test suite for Belvedere, following pytest best practices.

## Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_config.py           # Tests for configuration management
├── test_rule_engine.py      # Tests for rule evaluation and file operations
└── test_file_monitor.py     # Tests for file monitoring and event handling
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_config.py
```

### Run Specific Test Class

```bash
pytest tests/test_config.py::TestFolderManagement
```

### Run Specific Test

```bash
pytest tests/test_config.py::TestFolderManagement::test_add_folder_succeeds
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Run with Coverage Report

```bash
# Terminal report
pytest --cov=belvedere --cov-report=term-missing

# HTML report (view in htmlcov/index.html)
pytest --cov=belvedere --cov-report=html
```

## Test Organization

### Test Classes

Tests are organized into classes that group related functionality:

- **TestConfigInitialization**: Tests for Config class initialization
- **TestFolderManagement**: Tests for folder operations
- **TestRuleManagement**: Tests for rule CRUD operations
- **TestPreferences**: Tests for preference management
- **TestPersistence**: Tests for configuration save/load
- **TestRuleEvaluation**: Tests for rule matching logic
- **TestNameConditions**: Tests for name-based conditions
- **TestExtensionConditions**: Tests for extension-based conditions
- **TestSizeConditions**: Tests for size-based conditions
- **TestDateConditions**: Tests for date-based conditions
- **TestFileActions**: Tests for file operations (move, copy, rename, delete)
- **TestEventHandler**: Tests for file system event handling
- **TestIntegrationScenarios**: Integration tests for complete workflows

### Test Naming Convention

All test functions follow the pattern: `test_<what>_<condition>_<expected_result>`

Examples:
- `test_add_folder_succeeds`
- `test_move_file_fails_if_destination_not_exists`
- `test_evaluate_rule_all_match_type_requires_all_true`

## Fixtures

Shared fixtures are defined in `conftest.py`:

- **temp_dir**: Temporary directory for test files
- **temp_config_path**: Temporary config file path
- **config**: Config instance with temporary storage
- **rule_engine**: RuleEngine instance
- **file_monitor**: FileMonitor instance (auto-cleanup)
- **sample_file**: Sample test file
- **sample_rule**: Sample rule configuration
- **dest_dir**: Destination directory for file operations

## Test Markers

Tests can be marked for categorization:

- `@pytest.mark.unit`: Unit tests (testing single components)
- `@pytest.mark.integration`: Integration tests (testing multiple components)
- `@pytest.mark.slow`: Tests that take longer to execute

## Best Practices Followed

### AAA Pattern (Arrange, Act, Assert)

All tests follow the AAA pattern for clarity:

```python
def test_add_folder_succeeds(self, config):
    # Arrange
    test_folder = "/tmp/test_folder"
    
    # Act
    config.add_folder(test_folder)
    
    # Assert
    assert test_folder in config.get_folders()
```

### Descriptive Test Names

Test names clearly describe what's being tested:

```python
def test_move_file_respects_overwrite_flag(self, rule_engine, temp_dir, dest_dir):
    """Test that move respects overwrite flag when file exists."""
```

### Parametrized Tests

Multiple scenarios are tested efficiently:

```python
@pytest.mark.parametrize("subject,verb,obj,expected", [
    ('Name', 'is', 'test_document', True),
    ('Name', 'is', 'wrong_name', False),
    ('Extension', 'is', 'txt', True),
    ('Extension', 'is', 'pdf', False),
], ids=['name_match', 'name_mismatch', 'ext_match', 'ext_mismatch'])
def test_various_condition_combinations(self, rule_engine, sample_file, subject, verb, obj, expected):
    # Test implementation
```

### Mocking External Dependencies

External services and system calls are mocked:

```python
def test_recycle_file_succeeds(self, rule_engine, sample_file, mocker):
    """Test sending a file to recycle bin."""
    mock_send2trash = mocker.patch('belvedere.rule_engine.send2trash.send2trash')
    rule = {'action': 'Send file to Recycle Bin'}
    
    result = rule_engine.execute_action(sample_file, rule)
    
    assert result is True
    mock_send2trash.assert_called_once_with(str(sample_file))
```

### Independent Tests

Each test can run in isolation without dependencies on other tests:

```python
def test_delete_user(self):
    user = create_user()  # Create fresh user for this test
    delete_user(user)
    assert not user_exists(user.id)
```

### Edge Cases and Error Handling

Tests cover edge cases and error conditions:

```python
def test_remove_nonexistent_folder_does_nothing(self, config):
    """Test that removing non-existent folder doesn't cause errors."""
    test_folder = "/tmp/nonexistent_folder"
    config.remove_folder(test_folder)
    assert test_folder not in config.get_folders()
```

## Coverage

The test suite achieves:
- **Config module**: 97% coverage
- **RuleEngine module**: 82% coverage
- **FileMonitor module**: 89% coverage

Run `pytest --cov=belvedere --cov-report=html` to generate a detailed coverage report.

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```bash
# Install dependencies
pip install -e .[dev]

# Run tests with coverage
pytest --cov=belvedere --cov-report=xml

# Check if tests pass
echo $?  # Should be 0
```

## Adding New Tests

When adding new functionality:

1. Create tests first (TDD approach)
2. Follow existing naming conventions
3. Use appropriate fixtures from conftest.py
4. Add new shared fixtures to conftest.py if needed
5. Group related tests in classes
6. Use descriptive names and docstrings
7. Test both success and failure cases
8. Mock external dependencies
9. Ensure tests are independent

Example:

```python
class TestNewFeature:
    """Tests for the new feature."""
    
    def test_new_feature_succeeds_with_valid_input(self, fixture_name):
        """Test that new feature works with valid input."""
        # Arrange
        input_data = create_test_data()
        
        # Act
        result = new_feature(input_data)
        
        # Assert
        assert result.is_valid()
    
    def test_new_feature_raises_error_with_invalid_input(self, fixture_name):
        """Test that new feature raises error with invalid input."""
        # Arrange
        invalid_data = create_invalid_data()
        
        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            new_feature(invalid_data)
```

## Troubleshooting

### Tests Fail Locally

1. Ensure all dependencies are installed: `pip install -e .[dev]`
2. Check Python version: `python --version` (requires >=3.9)
3. Clear pytest cache: `pytest --cache-clear`

### Coverage Not Accurate

1. Ensure source code is in the correct location
2. Run: `pytest --cov=belvedere --cov-report=term-missing`
3. Check `.coveragerc` or `pyproject.toml` configuration

### Tests Hang

1. Check for file handles not being closed
2. Ensure FileMonitor instances are properly stopped
3. Use fixture cleanup (already implemented in conftest.py)

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
