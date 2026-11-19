# API Testing Framework Setup Guide - Siemens Energy Project

## Table of Contents
1. [Framework Overview](#framework-overview)
2. [Architecture](#architecture)
3. [Setup Instructions](#setup-instructions)
4. [Test Organization](#test-organization)
5. [DevOps Integration](#devops-integration)
6. [Best Practices](#best-practices)

---

## Framework Overview

### Technology Stack
- **Testing Framework**: Pytest
- **API Client**: FastAPI TestClient / Requests
- **Test Generation**: OpenAPI-based automated test generation
- **Reporting**: pytest-html, Allure
- **CI/CD**: Azure DevOps (Azure Pipelines)
- **Database**: PostgreSQL (with test isolation)
- **Containerization**: Docker & Docker Compose

### Key Features
✅ **Single Repository**: All test cases in one repo  
✅ **OpenAPI-Driven**: Automated test generation from OpenAPI specs  
✅ **Modular Structure**: Separate manual and generated tests  
✅ **Environment Management**: Multi-environment support (dev, staging, prod)  
✅ **Parallel Execution**: Pytest-xdist for faster test runs  
✅ **Comprehensive Reporting**: HTML, Allure, and JUnit reports  
✅ **CI/CD Ready**: Azure DevOps pipeline integration  

---

## Architecture

```
FASTAPI/
├── app/                          # Application code
├── tests/                        # Manual test cases
│   ├── conftest.py              # Shared fixtures
│   ├── test_*.py                # Manual tests
│   └── testdata/                # Test data files
├── generator/                    # Test generation engine
│   ├── pytest_api_test_generator.py
│   ├── test.json                # OpenAPI spec
│   └── generated-tests/         # Auto-generated tests
├── config/                       # Environment configs
│   ├── dev.env
│   ├── staging.env
│   └── prod.env
├── reports/                      # Test reports
├── .devops/                      # Azure DevOps pipelines
│   ├── azure-pipelines.yml
│   └── test-pipeline.yml
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Dependencies
└── docker-compose.yml            # Container orchestration
```

---

## Setup Instructions

### 1. Prerequisites
```powershell
# Install Python 3.9+
python --version

# Install Docker Desktop
docker --version
docker-compose --version
```

### 2. Clone and Setup
```powershell
# Navigate to project
cd "c:\Users\z00556rs\Documents\FASTAPI"

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 3. Environment Configuration
```powershell
# Copy environment template
cp config\dev.env.template config\dev.env

# Edit with your values
notepad config\dev.env
```

### 4. Database Setup
```powershell
# Start PostgreSQL via Docker
docker-compose up -d postgres

# Run migrations
alembic upgrade head
```

### 5. Run Tests
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test suite
pytest tests/test_posts.py

# Run generated tests
pytest generator/generated-tests/

# Run with parallel execution
pytest -n auto
```

---

## Test Organization

### Directory Structure

#### **tests/** - Manual Test Cases
- **Purpose**: Hand-crafted, business-logic specific tests
- **When to use**: Complex scenarios, integration tests, edge cases
- **Structure**:
  ```
  tests/
  ├── conftest.py              # Fixtures, hooks
  ├── test_post.py             # Post endpoints
  ├── test_users.py            # User management
  ├── test_votes.py            # Voting functionality
  └── testdata/                # JSON test data
  ```

#### **generator/generated-tests/** - Auto-Generated Tests
- **Purpose**: OpenAPI-driven CRUD tests
- **When to use**: Standard API operations, regression testing
- **Regeneration**: Run generator script when API changes

### Test Data Management
- **Static Data**: `tests/testdata/*.json`
- **Dynamic Data**: Fixtures in `conftest.py`
- **Test Isolation**: Each test uses fresh database via fixtures

---

## DevOps Integration

### Azure DevOps Setup

#### 1. Pipeline Configuration
The framework includes Azure Pipelines for:
- ✅ Automated test execution on commit/PR
- ✅ Multi-environment testing
- ✅ Test report generation and publishing
- ✅ Code coverage tracking
- ✅ Docker image building

#### 2. Pipeline Triggers
- **Continuous Integration**: On push to main/develop
- **Pull Request Validation**: On PR creation
- **Scheduled Runs**: Nightly regression tests
- **Manual Triggers**: On-demand test execution

#### 3. Test Reporting
- **JUnit XML**: For Azure DevOps test results
- **HTML Reports**: Published as pipeline artifacts
- **Allure Reports**: Interactive test reports
- **Coverage Reports**: Code coverage metrics

### Integration Steps

1. **Connect Repository to Azure DevOps**
   ```bash
   # Azure DevOps Project > Repos > Import Repository
   Repository URL: <your-git-url>
   ```

2. **Create Pipeline**
   ```bash
   # Azure DevOps > Pipelines > New Pipeline
   # Select: Existing Azure Pipelines YAML file
   # Path: .devops/azure-pipelines.yml
   ```

3. **Configure Variables**
   - DATABASE_HOSTNAME
   - DATABASE_PASSWORD
   - SECRET_KEY
   - BASE_URL_APP

4. **Enable Test Results**
   - Pipeline will automatically publish test results
   - View in: Pipelines > <Your Pipeline> > Test Results

---

## Best Practices

### 1. Test Organization
✅ **Single Responsibility**: One test function per scenario  
✅ **Clear Naming**: `test_<action>_<expected_outcome>`  
✅ **Independent Tests**: No dependencies between tests  
✅ **Fast Execution**: Use fixtures for setup, avoid unnecessary API calls  

### 2. Data Management
✅ **Test Data Isolation**: Each test creates its own data  
✅ **Cleanup**: Use fixtures with teardown  
✅ **Realistic Data**: Use production-like test data  

### 3. Version Control
✅ **Commit Generated Tests**: Track changes in API  
✅ **Separate Branches**: Feature branches for test development  
✅ **Code Review**: Peer review for test code  

### 4. Maintenance
✅ **Regenerate on API Changes**: Update generated tests  
✅ **Update Manual Tests**: Maintain custom test logic  
✅ **Monitor Flaky Tests**: Fix unreliable tests immediately  
✅ **Regular Cleanup**: Remove obsolete tests  

### 5. CI/CD Integration
✅ **Fast Feedback**: Keep test suite under 5 minutes  
✅ **Parallel Execution**: Use pytest-xdist  
✅ **Fail Fast**: Stop on first critical failure  
✅ **Clear Reports**: Descriptive failure messages  

---

## Monitoring and Reporting

### Test Metrics to Track
1. **Test Coverage**: Target 80%+ API coverage
2. **Pass Rate**: Monitor test stability
3. **Execution Time**: Optimize slow tests
4. **Failure Trends**: Identify flaky tests

### Azure DevOps Dashboards
- Test pass/fail trends
- Code coverage over time
- Test duration metrics
- Failure analysis

---

## Troubleshooting

### Common Issues

**Issue**: Tests fail locally but pass in CI
- **Solution**: Check environment variables, database state

**Issue**: Slow test execution
- **Solution**: Enable parallel execution (`pytest -n auto`)

**Issue**: Database connection errors
- **Solution**: Verify Docker containers are running

**Issue**: Test data conflicts
- **Solution**: Ensure proper fixture scoping and cleanup

---

## Additional Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **Azure Pipelines**: https://docs.microsoft.com/en-us/azure/devops/pipelines/

---

## Support

For questions or issues:
1. Check documentation above
2. Review generated test examples
3. Contact: [Your Team Email]

---

**Last Updated**: November 2025  
**Version**: 1.0  
**Maintained by**: Siemens Energy Testing Team
