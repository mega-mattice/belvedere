# Development Guide

This guide covers development setup, coding standards, and contribution guidelines for Belvedere.

## Development Setup

1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```

2. **Clone and setup the project**:
   ```bash
   git clone https://github.com/mega-mattice/belvedere.git
   cd belvedere
   poetry install
   ```

3. **Install pre-commit hooks**:
   ```bash
   poetry run pre-commit install
   ```

## Code Quality

Belvedere uses automated tools to maintain code quality:

### Pre-commit Hooks

Pre-commit hooks run automatically on each commit and ensure code meets quality standards:

- **Black**: Code formatting (line length: 127 chars)
- **isort**: Import sorting (Black-compatible profile)
- **flake8**: Python linting (max line length: 127, ignores E203, W503)
- **General**: Trailing whitespace removal, end-of-file fixes, YAML validation

### Running Quality Checks

Run all pre-commit hooks manually:
```bash
poetry run pre-commit run --all-files
```

Run individual tools:
```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Lint code
poetry run flake8 .
```

### CI/CD Integration

The same quality checks run in GitHub Actions on every push and pull request to the `main` branch. Pre-commit hooks ensure your local code passes these checks before committing.

## Testing

Run the test suite:
```bash
# Run all tests
python test_belvedere.py

# Run with pytest (includes coverage)
poetry run pytest
```

## Building

See [Building Guide](building.md) for instructions on building executables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper tests
4. Ensure pre-commit hooks pass
5. Submit a pull request

All contributions must pass the automated quality checks and include appropriate tests.
