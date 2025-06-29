# TODO List for Gimeltra

## Critical Fixes
- [ ] Resolve license inconsistency between README.md (MIT) and setup.py (GPLv2)
- [ ] Update version number from 1.0.0 to 1.1.0
- [ ] Fix any deprecation warnings in dependencies

## Testing
- [ ] Create test directory structure
- [ ] Write unit tests for Transliterator class
- [ ] Write tests for each script conversion
- [ ] Add tests for CLI functionality
- [ ] Add tests for edge cases (empty strings, invalid scripts)
- [ ] Set up pytest configuration
- [ ] Add coverage reporting

## Documentation
- [ ] Add comprehensive docstrings to all functions and classes
- [ ] Create API documentation using Sphinx
- [ ] Add more usage examples to README
- [ ] Document transliteration rules and conventions
- [ ] Create CONTRIBUTING.md
- [ ] Add badges to README (build, coverage, version)

## Code Quality
- [ ] Add type hints throughout the codebase
- [ ] Implement proper error handling and custom exceptions
- [ ] Add input validation for scripts and text
- [ ] Replace print statements with proper logging
- [ ] Add code formatting with black/ruff
- [ ] Set up pre-commit hooks

## CI/CD
- [ ] Create GitHub Actions workflow for testing
- [ ] Add workflow for code quality checks
- [ ] Set up automated PyPI deployment
- [ ] Add multi-Python version testing (3.9-3.12)
- [ ] Add security scanning

## Deployment
- [ ] Create Dockerfile
- [ ] Add docker-compose.yml for easy setup
- [ ] Create PyInstaller spec for standalone executable
- [ ] Ensure proper wheel generation
- [ ] Consider conda-forge package

## Dependencies
- [ ] Evaluate if yaplon is necessary
- [ ] Pin all dependency versions
- [ ] Add optional dependencies for development
- [ ] Create requirements-dev.txt

## Features
- [ ] Add batch file processing
- [ ] Implement progress bars for long operations
- [ ] Add JSON output format option
- [ ] Create REST API wrapper
- [ ] Add configuration file support

## Performance
- [ ] Profile code to identify bottlenecks
- [ ] Optimize regular expression usage
- [ ] Consider lazy loading for JSON data
- [ ] Add caching for common conversions

## Project Structure
- [ ] Reorganize code into logical modules
- [ ] Separate CLI from library code
- [ ] Create dedicated config module
- [ ] Add __all__ exports properly

## Data Management
- [ ] Validate JSON data on load
- [ ] Add data integrity checks
- [ ] Document data format specification
- [ ] Create tool for data validation

## Community
- [ ] Set up issue templates
- [ ] Create pull request template
- [ ] Add code of conduct
- [ ] Set up discussions/wiki