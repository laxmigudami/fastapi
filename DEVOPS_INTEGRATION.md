# Azure DevOps Integration Guide
# Siemens Energy API Testing Framework

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Repository Setup](#repository-setup)
4. [Pipeline Configuration](#pipeline-configuration)
5. [Variable Groups](#variable-groups)
6. [Test Execution](#test-execution)
7. [Reporting](#reporting)
8. [Best Practices](#best-practices)

---

## Overview

This guide explains how to integrate the API testing framework with Azure DevOps for:
- ✅ Automated test execution on code changes
- ✅ Pull request validation
- ✅ Scheduled regression testing
- ✅ Multi-environment testing
- ✅ Test result tracking and reporting
- ✅ Code coverage monitoring

---

## Prerequisites

### Azure DevOps Setup
1. **Azure DevOps Organization**: Access to Siemens Energy Azure DevOps
2. **Project**: Create or use existing project
3. **Permissions**: 
   - Build Administrator (to create pipelines)
   - Contributor (to push code)
   - Project Administrator (to manage variables)

### Repository Requirements
- Git repository initialized
- All code committed to main/develop branch
- `.devops/azure-pipelines.yml` present

---

## Repository Setup

### Step 1: Push Code to Azure Repos

```powershell
# Navigate to your project
cd "c:\Users\z00556rs\Documents\FASTAPI"

# Initialize git (if not already done)
git init

# Add Azure DevOps remote
git remote add origin https://dev.azure.com/siemens-energy/<project-name>/_git/<repo-name>

# Add all files
git add .

# Commit
git commit -m "Initial commit: API Testing Framework setup"

# Push to Azure DevOps
git push -u origin main
```

### Step 2: Verify Repository Structure

Ensure these files are present:
```
✅ .devops/azure-pipelines.yml
✅ pytest.ini
✅ requirements.txt
✅ requirements-test.txt
✅ tests/conftest.py
✅ config/*.env
```

---

## Pipeline Configuration

### Step 1: Create Pipeline in Azure DevOps

1. **Navigate to Pipelines**
   - Go to Azure DevOps project
   - Click **Pipelines** > **New Pipeline**

2. **Select Repository**
   - Choose **Azure Repos Git**
   - Select your repository

3. **Configure Pipeline**
   - Select **Existing Azure Pipelines YAML file**
   - Path: `.devops/azure-pipelines.yml`
   - Click **Continue**

4. **Review and Run**
   - Review the YAML content
   - Click **Run** to execute first time

### Step 2: Pipeline Features

The pipeline includes:

#### **Triggers**
```yaml
# Automatic triggers on:
- Push to main, develop, feature/*
- Pull requests to main, develop
- Scheduled nightly runs (2 AM)
```

#### **Stages**
1. **Build**: Setup environment, install dependencies, code linting
2. **Test**: Run manual & generated tests with coverage
3. **Report**: Generate Allure and HTML reports
4. **Deploy**: Deploy to environments (DEV only from main branch)

#### **Services**
- PostgreSQL container for database tests
- Can add Redis, RabbitMQ, etc. as needed

---

## Variable Groups

### Step 1: Create Variable Group

1. **Navigate to Library**
   - Go to **Pipelines** > **Library**
   - Click **+ Variable group**

2. **Create Group: api-test-variables**
   ```
   Name: api-test-variables
   Description: Variables for API testing framework
   ```

3. **Add Variables**

#### Required Variables
| Variable Name | Value | Secret? | Description |
|--------------|-------|---------|-------------|
| `SECRET_KEY` | `<your-secret-key>` | ✅ | JWT secret key |
| `DATABASE_PASSWORD` | `password123` | ✅ | Database password |
| `OPENAI_API_KEY` | `<your-key>` | ✅ | OpenAI API key (optional) |
| `DEV_BASE_URL` | `http://api-dev.example.com` | ❌ | DEV environment URL |
| `STAGING_BASE_URL` | `http://api-staging.example.com` | ❌ | Staging URL |
| `PROD_BASE_URL` | `https://api.example.com` | ❌ | Production URL |

#### Optional Variables
| Variable Name | Value | Description |
|--------------|-------|-------------|
| `PYTEST_WORKERS` | `auto` | Number of parallel workers |
| `TEST_TIMEOUT` | `300` | Test timeout in seconds |
| `COVERAGE_THRESHOLD` | `70` | Minimum coverage percentage |

### Step 2: Link Variable Group to Pipeline

The pipeline already references the variable group:
```yaml
variables:
  - group: api-test-variables
```

No additional configuration needed!

---

## Test Execution

### Automatic Execution

#### On Pull Request
```yaml
# Tests run automatically when:
- Creating a new PR
- Pushing commits to existing PR
- PR targets main or develop branch

# Results appear in:
- PR conversation tab
- Checks section
```

#### On Push to Main/Develop
```yaml
# Full test suite runs on:
- Direct pushes to main/develop
- PR merge to main/develop

# Includes:
- Unit tests
- Integration tests
- Generated tests
- Code coverage
```

#### Scheduled Runs
```yaml
# Nightly regression tests:
- Time: 2:00 AM (configurable)
- Frequency: Daily
- Branch: main
- Full test suite with reporting
```

### Manual Execution

#### Run Pipeline Manually
1. Go to **Pipelines**
2. Select your pipeline
3. Click **Run pipeline**
4. Choose:
   - Branch
   - Variables (override if needed)
5. Click **Run**

#### Run Specific Tests
```powershell
# Modify pipeline to run specific markers
# Add in variables section:
pytest.markers: 'smoke'

# Or override in manual run
```

---

## Reporting

### Test Results

#### In Azure DevOps
1. **Test Tab**
   - Pipeline run > Tests tab
   - View pass/fail counts
   - Drill down to specific failures
   - View test history trends

2. **Test Analytics**
   - Go to **Test Plans** > **Runs**
   - View aggregated test results
   - Identify flaky tests
   - Track test duration

#### Published Reports

##### HTML Report
```yaml
# Location: Pipeline Artifacts
1. Pipeline run > Artifacts
2. Download 'coverage-report'
3. Open index.html in browser
```

##### Allure Report
```yaml
# Generate after test run:
1. Download allure-results artifact
2. Install Allure: npm install -g allure-commandline
3. Generate: allure serve allure-results
```

### Code Coverage

#### View Coverage
```yaml
# Coverage reports published to:
1. Pipeline run > Code Coverage tab
2. View coverage percentage
3. Drill down to file level
4. Track coverage trends
```

#### Coverage Requirements
```yaml
# Set minimum coverage threshold:
# In pytest.ini or azure-pipelines.yml
--cov-fail-under=70
```

### Notifications

#### Configure Email Notifications
1. **Pipeline Settings** > **Notifications**
2. Add notifications for:
   - ✅ Build completed
   - ❌ Build failed
   - 📊 Test failures
   - 📈 Coverage drops

#### Teams/Slack Integration
```yaml
# Add webhook notifications:
# Install Azure DevOps app in Teams/Slack
# Configure channel notifications
```

---

## Best Practices

### 1. Branch Strategy

```yaml
# Recommended Git Flow:
main (production-ready)
├── develop (integration branch)
├── feature/* (feature branches)
├── bugfix/* (bug fixes)
└── hotfix/* (urgent fixes)

# Pipeline behavior:
- feature/*: Run smoke tests only
- develop: Run full test suite
- main: Full suite + deployment
```

### 2. Test Organization

```yaml
# Use markers for selective execution:
@pytest.mark.smoke      # Critical paths
@pytest.mark.regression # Full test suite
@pytest.mark.slow       # Long-running tests

# Pipeline stages:
PR Validation: smoke tests (fast feedback)
Nightly Runs: regression tests (comprehensive)
```

### 3. Environment Management

```yaml
# Separate configurations:
- DEV: Full CRUD operations allowed
- STAGING: Production-like testing
- PROD: Read-only smoke tests

# Use environment-specific variable groups:
- api-test-dev
- api-test-staging
- api-test-prod
```

### 4. Test Data Management

```yaml
# Strategies:
1. Use fixtures for test data creation
2. Clean up after tests (in teardown)
3. Use transaction rollback for database tests
4. Avoid hardcoded IDs (use dynamic creation)

# In conftest.py:
@pytest.fixture(scope="function")
def cleanup():
    yield
    # Cleanup logic here
```

### 5. Pipeline Optimization

```yaml
# Speed up pipeline:
1. Cache dependencies (pip cache)
2. Run tests in parallel (-n auto)
3. Use pytest-xdist
4. Skip slow tests in PR validation
5. Use Docker layer caching

# Example:
pytest -n auto -m "not slow" --lf
```

### 6. Monitoring and Alerts

```yaml
# Set up monitoring for:
- Test pass rate trends
- Test execution duration
- Flaky test identification
- Coverage trends
- Build failure rates

# Use Azure DevOps Analytics:
- Create custom dashboards
- Track KPIs
- Set alert thresholds
```

---

## Troubleshooting

### Common Issues

#### 1. Pipeline Fails to Start
```yaml
# Check:
- YAML syntax is valid
- Variable group is linked
- Agent pool is available

# Fix:
- Validate YAML online
- Verify variable group permissions
- Check agent pool availability
```

#### 2. Tests Fail in Pipeline but Pass Locally
```yaml
# Check:
- Environment variables match
- Database is accessible
- Dependencies are installed
- Python version matches

# Fix:
- Print environment variables in pipeline
- Verify service connections
- Check requirements.txt
```

#### 3. Timeout Issues
```yaml
# If tests timeout:
- Increase TEST_TIMEOUT variable
- Add --timeout=600 to pytest command
- Check for hanging tests
- Verify external service availability
```

#### 4. Database Connection Errors
```yaml
# Check:
- PostgreSQL service is running
- Connection string is correct
- Database port is exposed
- Network connectivity

# Fix:
- Add wait-for-it script
- Verify service health before tests
```

---

## Advanced Configuration

### Multi-Stage Pipelines

```yaml
# Create environment-specific stages:
stages:
  - stage: TestDev
    environment: DEV
    jobs:
      - job: RunTests
        steps:
          - script: pytest -m smoke
  
  - stage: TestStaging
    environment: STAGING
    dependsOn: TestDev
    jobs:
      - job: RunTests
        steps:
          - script: pytest -m regression
```

### Approval Gates

```yaml
# Add manual approvals:
1. Go to Environments
2. Select environment (e.g., STAGING)
3. Add Approval check
4. Assign approvers

# Pipeline will wait for approval before deployment
```

### Matrix Testing

```yaml
# Test against multiple Python versions:
strategy:
  matrix:
    Python39:
      python.version: '3.9'
    Python310:
      python.version: '3.10'
    Python311:
      python.version: '3.11'
```

---

## Summary Checklist

Before going live:

- [ ] Repository pushed to Azure DevOps
- [ ] Pipeline YAML file present
- [ ] Variable group created and configured
- [ ] All secrets added securely
- [ ] Pipeline tested manually
- [ ] Test results publishing verified
- [ ] Coverage reports working
- [ ] Notifications configured
- [ ] Branch policies set
- [ ] Team members notified

---

## Contact & Support

**Questions?**
- Team Lead: [Name]
- DevOps Support: [Email/Teams]
- Documentation: [Wiki Link]

**Updates:**
Last Updated: November 2025
Version: 1.0
