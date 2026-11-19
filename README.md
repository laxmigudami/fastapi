# Siemens Energy API Testing Framework

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.4+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-teal.svg)
![License](https://img.shields.io/badge/License-Siemens-orange.svg)

**Comprehensive API Testing Framework with OpenAPI-Driven Test Generation**

[Quick Start](#-quick-start) • [Documentation](#-documentation) • [Features](#-features) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [Project Structure](#-project-structure)
- [Test Development](#-test-development)
- [CI/CD Integration](#-cicd-integration)
- [Best Practices](#-best-practices)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🎯 Overview

This repository contains the comprehensive API testing framework for Siemens Energy projects. It combines manual test development with automated test generation from OpenAPI specifications, providing a robust solution for API quality assurance.

### Key Capabilities

- 🤖 **Automated Test Generation**: Generate pytest tests from OpenAPI/Swagger specs
- 🔄 **CI/CD Ready**: Full Azure DevOps integration with pipelines
- 🎯 **Multi-Environment**: Support for DEV, Staging, and Production
- 📊 **Rich Reporting**: HTML, Allure, JUnit, and coverage reports
- ⚡ **Parallel Execution**: Fast test runs with pytest-xdist
- 🗃️ **Single Repository**: All test cases maintained in one place
- 🔐 **Security Testing**: Authentication and authorization validation
- 🐳 **Docker Support**: Containerized test execution

---

## ✨ Features

### Test Generation
- ✅ OpenAPI 3.x specification parsing
- ✅ Automatic CRUD test generation
- ✅ Positive and negative test scenarios
- ✅ Authentication testing
- ✅ Schema validation

### Test Execution
- ✅ Pytest framework
- ✅ Parallel test execution
- ✅ Test markers for categorization
- ✅ Fixture-based test data
- ✅ Database transaction isolation

### Reporting & Analytics
- ✅ HTML test reports
- ✅ Allure interactive reports
- ✅ Code coverage metrics
- ✅ JUnit XML for CI/CD
- ✅ Test trend analysis

### DevOps Integration
- ✅ Azure Pipelines configuration
- ✅ Automated PR validation
- ✅ Scheduled regression testing
- ✅ Multi-environment deployment
- ✅ Test result publishing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   API Testing Framework                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Manual     │    │  Generated   │    │    Test      │ │
│  │    Tests     │    │    Tests     │    │   Runner     │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│         │                    │                    │         │
│         └────────────────────┴────────────────────┘         │
│                            │                                 │
│                    ┌───────▼────────┐                       │
│                    │  Pytest Engine  │                       │
│                    └───────┬────────┘                       │
│                            │                                 │
│         ┌──────────────────┼──────────────────┐            │
│         │                  │                  │            │
│    ┌────▼────┐       ┌────▼────┐       ┌────▼────┐       │
│    │ FastAPI │       │Database │       │ Reports │       │
│    │TestClient│       │ (Postgres)│      │Generation│       │
│    └─────────┘       └─────────┘       └─────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   Azure DevOps   │
                  │    Pipelines     │
                  └──────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

```powershell
# Required software:
- Python 3.9 or higher
- PostgreSQL 12+
- Docker Desktop (optional)
- Git

# Verify installations:
python --version
docker --version
git --version
```

### Installation

```powershell
# 1. Clone the repository
git clone https://dev.azure.com/siemens-energy/<project>/_git/<repo>
cd FASTAPI

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# 4. Setup environment configuration
cp config\.env.template config\dev.env
# Edit config\dev.env with your settings

# 5. Start database (Docker)
docker-compose up -d postgres

# 6. Run database migrations
alembic upgrade head

# 7. Run tests
pytest tests/ -v
```

### Quick Test Run

```powershell
# Run all tests
python run_tests.py --all

# Run smoke tests
python run_tests.py --markers smoke

# Run with coverage
python run_tests.py --all --coverage --html-report

# Run in parallel
python run_tests.py --all --parallel
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Framework Setup Guide](FRAMEWORK_SETUP_GUIDE.md) | Complete framework setup and configuration |
| [DevOps Integration](DEVOPS_INTEGRATION.md) | Azure DevOps pipeline setup and usage |
| [Test Commands](TEST_COMMANDS.md) | Comprehensive pytest command reference |
| [API Documentation](docs/API.md) | API endpoints and usage |

---

## 📁 Project Structure

```
FASTAPI/
├── 📱 app/                          # Application source code
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   ├── models.py                    # Database models
│   ├── schemas.py                   # Pydantic schemas
│   ├── database.py                  # Database configuration
│   ├── config.py                    # App configuration
│   ├── oauth2.py                    # Authentication
│   └── routers/                     # API route handlers
│       ├── auth.py
│       ├── post.py
│       ├── user.py
│       └── vote.py
│
├── 🧪 tests/                        # Manual test cases
│   ├── conftest.py                  # Pytest fixtures & hooks
│   ├── test_post.py                 # Post endpoint tests
│   ├── test_users.py                # User endpoint tests
│   ├── test_votes.py                # Vote endpoint tests
│   └── testdata/                    # Test data files
│       └── users.json
│
├── 🤖 generator/                    # Test generation engine
│   ├── pytest_api_test_generator.py # Test generator script
│   ├── test.json                    # OpenAPI specification
│   ├── generated-tests/             # Auto-generated tests
│   │   ├── test_login.py
│   │   ├── test_posts.py
│   │   ├── test_users.py
│   │   └── test_vote.py
│   └── utils/
│       └── openai.py                # OpenAI integration
│
├── ⚙️ config/                       # Environment configurations
│   ├── .env.template                # Environment template
│   ├── dev.env                      # Development config
│   ├── staging.env                  # Staging config
│   └── prod.env                     # Production config
│
├── 🔄 .devops/                      # CI/CD pipelines
│   └── azure-pipelines.yml          # Azure DevOps pipeline
│
├── 🗄️ alembic/                      # Database migrations
│   ├── env.py
│   └── versions/
│
├── 📊 reports/                      # Test reports (generated)
├── 📝 logs/                         # Test logs (generated)
├── 🐳 docker-compose.yml            # Docker services
├── 📋 pytest.ini                    # Pytest configuration
├── 📦 requirements.txt              # Python dependencies
├── 📦 requirements-test.txt         # Test dependencies
├── 🏃 run_tests.py                  # Test runner script
└── 📖 README.md                     # This file
```

---

## 🔬 Test Development

### Manual Tests

Create tests in `tests/` directory:

```python
# tests/test_example.py
import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    """Test retrieving all posts"""
    res = authorized_client.get("/posts/")
    
    assert res.status_code == 200
    posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts) > 0

@pytest.mark.smoke
def test_create_post(authorized_client):
    """Test creating a new post"""
    res = authorized_client.post(
        "/posts/",
        json={"title": "Test", "content": "Test content"}
    )
    
    assert res.status_code == 201
    post = schemas.PostOut(**res.json())
    assert post.title == "Test"
```

### Generated Tests

Generate tests from OpenAPI spec:

```powershell
# 1. Update OpenAPI spec
# Edit generator/test.json

# 2. Generate tests
python generator/pytest_api_test_generator.py

# 3. Run generated tests
pytest generator/generated-tests/ -v
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.smoke      # Critical functionality
@pytest.mark.regression # Full regression suite
@pytest.mark.integration# Integration tests
@pytest.mark.slow       # Long-running tests
@pytest.mark.auth       # Authentication tests
@pytest.mark.negative   # Negative test cases
```

---

## 🔄 CI/CD Integration

### Azure DevOps Pipeline

The framework includes a complete Azure Pipelines configuration:

**Triggers:**
- Push to main/develop/feature branches
- Pull requests
- Scheduled nightly runs (2 AM)

**Stages:**
1. **Build**: Setup, lint, dependencies
2. **Test**: Execute tests with coverage
3. **Report**: Generate and publish reports
4. **Deploy**: Deploy to environments

**Setup:**
```powershell
# 1. Push code to Azure Repos
git remote add origin <azure-repo-url>
git push -u origin main

# 2. Create pipeline in Azure DevOps
# Pipelines > New Pipeline > Existing YAML
# Path: .devops/azure-pipelines.yml

# 3. Configure variable group
# Pipelines > Library > + Variable group
# Name: api-test-variables
# Add required variables (see DEVOPS_INTEGRATION.md)

# 4. Run pipeline
# Pipelines > Select pipeline > Run
```

For detailed setup instructions, see [DEVOPS_INTEGRATION.md](DEVOPS_INTEGRATION.md)

---

## 💡 Best Practices

### 1. Test Organization
- ✅ One test file per API resource
- ✅ Use descriptive test names: `test_<action>_<expected_result>`
- ✅ Group related tests in classes
- ✅ Keep tests independent and idempotent

### 2. Test Data Management
- ✅ Use fixtures for test data creation
- ✅ Clean up after each test
- ✅ Use realistic test data
- ✅ Store reusable data in `tests/testdata/`

### 3. Assertions
- ✅ Assert status code first
- ✅ Validate response schema
- ✅ Check response data values
- ✅ Use descriptive assertion messages

### 4. Performance
- ✅ Run tests in parallel (`-n auto`)
- ✅ Use appropriate fixture scopes
- ✅ Mark slow tests with `@pytest.mark.slow`
- ✅ Skip unnecessary API calls

### 5. Maintenance
- ✅ Regenerate tests when API changes
- ✅ Update fixtures when data models change
- ✅ Review and remove obsolete tests
- ✅ Keep test dependencies updated

---

## 🐛 Troubleshooting

### Common Issues

#### Tests fail with database connection error
```powershell
# Ensure PostgreSQL is running
docker-compose up -d postgres

# Verify connection settings in config/dev.env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
```

#### Import errors in tests
```powershell
# Reinstall dependencies
pip install -r requirements.txt -r requirements-test.txt

# Verify Python environment
python -c "import pytest; print(pytest.__version__)"
```

#### Tests hang or timeout
```powershell
# Run with timeout
pytest --timeout=60

# Check for infinite loops or blocking operations
pytest -s  # Show print statements
```

#### Coverage report not generated
```powershell
# Install coverage
pip install pytest-cov

# Run with coverage flags
pytest --cov=app --cov-report=html
```

For more troubleshooting, see [FRAMEWORK_SETUP_GUIDE.md](FRAMEWORK_SETUP_GUIDE.md)

---

## 🤝 Contributing

### Development Workflow

1. **Create Feature Branch**
   ```powershell
   git checkout -b feature/new-test-suite
   ```

2. **Develop Tests**
   ```powershell
   # Write tests
   # Run locally
   pytest tests/test_new_feature.py -v
   ```

3. **Run Full Test Suite**
   ```powershell
   python run_tests.py --all --coverage
   ```

4. **Commit and Push**
   ```powershell
   git add .
   git commit -m "Add: New test suite for feature X"
   git push origin feature/new-test-suite
   ```

5. **Create Pull Request**
   - Pipeline runs automatically
   - Address any failures
   - Request code review

### Code Style

```powershell
# Format code
black tests/ app/

# Check style
flake8 tests/ app/ --max-line-length=120

# Sort imports
isort tests/ app/
```

---

## 📊 Reporting

### View Test Results

#### Locally
```powershell
# HTML report
pytest --html=reports/report.html --self-contained-html
# Open reports/report.html in browser

# Coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html

# Allure report
pytest --alluredir=allure-results
allure serve allure-results
```

#### Azure DevOps
- Pipeline Run > **Tests** tab (pass/fail counts)
- Pipeline Run > **Code Coverage** tab (coverage metrics)
- Pipeline Run > **Artifacts** (HTML reports)

---

## 📈 Metrics & KPIs

Track these metrics for test suite health:

| Metric | Target | Description |
|--------|--------|-------------|
| Test Coverage | ≥ 80% | Code coverage percentage |
| Test Pass Rate | ≥ 95% | Percentage of passing tests |
| Execution Time | < 5 min | Total test suite duration |
| Flaky Tests | < 2% | Tests with inconsistent results |
| API Coverage | 100% | Percentage of endpoints tested |

---

## 🔒 Security

- 🔐 Store secrets in Azure Key Vault
- 🔐 Use variable groups for sensitive data
- 🔐 Never commit credentials to repo
- 🔐 Rotate API keys regularly
- 🔐 Use read-only credentials for production

---

## 📞 Support

**Questions or Issues?**
- 📧 Email: [team-email@siemens-energy.com]
- 💬 Teams: [#api-testing-support]
- 📖 Wiki: [Internal Wiki Link]
- 🐛 Issues: [Azure DevOps Work Items]

---

## 📄 License

© 2025 Siemens Energy. Internal Use Only.

---

## 🎉 Acknowledgments

Built with:
- [Pytest](https://pytest.org/) - Testing framework
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Allure](https://docs.qameta.io/allure/) - Test reporting
- [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) - CI/CD

---

<div align="center">

**Made with ❤️ by Siemens Energy Testing Team**

[⬆ Back to Top](#siemens-energy-api-testing-framework)

</div>
