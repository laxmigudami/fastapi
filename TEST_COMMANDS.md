# Quick Test Commands for Siemens Energy API Testing
# Run these commands from PowerShell

# ============================================================================
# BASIC COMMANDS
# ============================================================================

# Run all tests
pytest

# Run specific test file
pytest tests/test_posts.py

# Run specific test function
pytest tests/test_posts.py::test_get_posts

# Run with verbose output
pytest -v

# Run with very verbose output
pytest -vv


# ============================================================================
# TEST SELECTION
# ============================================================================

# Run manual tests only
pytest tests/

# Run generated tests only
pytest generator/generated-tests/

# Run all tests
pytest tests/ generator/generated-tests/

# Run tests by marker
pytest -m smoke
pytest -m regression
pytest -m "not slow"
pytest -m "smoke or regression"


# ============================================================================
# PARALLEL EXECUTION
# ============================================================================

# Run tests in parallel (auto-detect CPUs)
pytest -n auto

# Run with specific number of workers
pytest -n 4

# Run tests with load balancing
pytest -n auto --dist loadscope


# ============================================================================
# COVERAGE REPORTING
# ============================================================================

# Run with coverage
pytest --cov=app

# Coverage with HTML report
pytest --cov=app --cov-report=html

# Coverage with terminal report
pytest --cov=app --cov-report=term-missing

# Coverage with XML (for CI/CD)
pytest --cov=app --cov-report=xml

# Coverage with minimum threshold
pytest --cov=app --cov-fail-under=70


# ============================================================================
# HTML REPORTS
# ============================================================================

# Generate HTML report
pytest --html=reports/pytest-report.html --self-contained-html

# HTML report with coverage
pytest --cov=app --cov-report=html --html=reports/pytest-report.html --self-contained-html


# ============================================================================
# ALLURE REPORTS
# ============================================================================

# Generate Allure results
pytest --alluredir=allure-results

# Generate and view Allure report
pytest --alluredir=allure-results; allure serve allure-results

# Generate static Allure report
pytest --alluredir=allure-results; allure generate allure-results --clean -o allure-report


# ============================================================================
# JUNIT XML (for CI/CD)
# ============================================================================

# Generate JUnit XML
pytest --junitxml=reports/junit.xml

# JUnit with test durations
pytest --junitxml=reports/junit.xml --junit-duration=total


# ============================================================================
# FAILURE HANDLING
# ============================================================================

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Run only last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff


# ============================================================================
# TEST FILTERING
# ============================================================================

# Run tests matching keyword
pytest -k "test_post"
pytest -k "test_get or test_post"
pytest -k "not slow"

# Run tests in specific directory
pytest tests/
pytest generator/generated-tests/


# ============================================================================
# DEBUGGING
# ============================================================================

# Show local variables on failure
pytest -l

# Show captured output
pytest -s

# Enter debugger on failure
pytest --pdb

# Enter debugger on first failure
pytest -x --pdb

# Show print statements
pytest -s


# ============================================================================
# USING THE TEST RUNNER
# ============================================================================

# Run all tests with runner
python run_tests.py --all

# Run manual tests with coverage
python run_tests.py --manual --coverage

# Run generated tests in parallel
python run_tests.py --generated --parallel

# Run smoke tests
python run_tests.py --all --markers smoke

# Run with HTML report
python run_tests.py --all --html-report

# Run specific environment
python run_tests.py --all --env staging

# Run with all reports
python run_tests.py --all --coverage --html-report --junit


# ============================================================================
# ENVIRONMENT-SPECIFIC RUNS
# ============================================================================

# Run against DEV
$env:ENV="dev"; pytest

# Run against STAGING
$env:ENV="staging"; pytest -m smoke

# Run against PROD (read-only smoke tests)
$env:ENV="prod"; pytest -m smoke


# ============================================================================
# CONTINUOUS INTEGRATION
# ============================================================================

# CI command (parallel, coverage, reports)
pytest tests/ -n auto --cov=app --cov-report=xml --cov-report=html --junitxml=reports/junit.xml --html=reports/pytest-report.html --self-contained-html

# Quick CI (smoke tests only)
pytest -m smoke -n auto --junitxml=reports/junit.xml


# ============================================================================
# TEST GENERATION
# ============================================================================

# Generate tests from OpenAPI spec
python generator/pytest_api_test_generator.py

# Validate generated tests
pytest generator/generated-tests/ --collect-only


# ============================================================================
# DOCKER COMMANDS
# ============================================================================

# Run tests in Docker
docker-compose run --rm api pytest

# Run with coverage in Docker
docker-compose run --rm api pytest --cov=app --cov-report=html

# Run specific tests in Docker
docker-compose run --rm api pytest tests/test_posts.py


# ============================================================================
# USEFUL COMBINATIONS
# ============================================================================

# Full test suite with reports (Recommended for CI)
pytest tests/ generator/generated-tests/ -n auto --cov=app --cov-report=html --cov-report=xml --html=reports/pytest-report.html --self-contained-html --junitxml=reports/junit.xml

# Quick smoke test
pytest -m smoke -v

# Comprehensive local testing
pytest tests/ -v --cov=app --cov-report=html --html=reports/pytest-report.html --self-contained-html

# Debug failing test
pytest tests/test_posts.py::test_specific_function -vv -s --pdb

# Regression testing
pytest -m regression -n auto --html=reports/regression-report.html
