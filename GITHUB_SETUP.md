# GitHub Actions CI/CD Setup Guide

## Overview
This guide walks you through setting up GitHub Actions for automated testing and deployment of your International Football EDA project using Databricks Asset Bundles.

## Workflows Created

### 1. PR Validation (`pr-validate.yml`)
**Triggers:** Pull requests to `main` or `develop` branches

**What it does:**
* Validates bundle configuration
* Generates bundle summary
* Comments on PR with validation results
* Lints notebook code

**Purpose:** Ensures code quality before merging

### 2. Run Tests (`run-tests.yml`)
**Triggers:** Pull requests and pushes to `develop`

**What it does:**
* Runs unit tests (if they exist)
* Deploys to dev environment
* Runs integration tests on Databricks

**Purpose:** Validates functionality before merging

### 3. Deploy (`deploy.yml`)
**Triggers:** 
* Push to `develop` → deploys to **staging**
* Push to `main` → deploys to **production**
* Manual workflow dispatch

**What it does:**
* Validates bundle
* Deploys to target environment
* Runs tests (staging only)
* Creates deployment summary

**Purpose:** Automated deployment to environments

## Setup Instructions

### Step 1: Create a Databricks Personal Access Token

1. Go to your Databricks workspace
2. Click your user profile (top right) → **Settings**
3. Go to **Developer** → **Access tokens**
4. Click **Generate new token**
5. Give it a name (e.g., "GitHub Actions CI/CD")
6. Set expiration (90 days recommended for security)
7. **Copy the token** (you won't see it again!)

### Step 2: Configure GitHub Repository Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value | Example |
|-------------|-------|---------|
| `DATABRICKS_HOST` | Your workspace URL | `https://dbc-569a476f-79ac.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Token from Step 1 | `dapi1234567890abcdef...` |

### Step 3: Configure GitHub Environments (Optional but Recommended)

For production deployments, set up environment protection:

1. Go to **Settings** → **Environments**
2. Create three environments:
   * `dev` (no protection)
   * `staging` (optional: require review)
   * `production` (require review from maintainers)

3. For `production` environment:
   * Click **Add deployment protection rule**
   * Select **Required reviewers**
   * Add team members who can approve production deploys

### Step 4: Set Up Branch Protection

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   * ✅ Require pull request reviews before merging
   * ✅ Require status checks to pass before merging
     * Add: `validate-bundle`
     * Add: `lint-notebooks`
     * Add: `unit-tests`
   * ✅ Require branches to be up to date before merging

3. Add rule for `develop` branch (similar settings, slightly relaxed)

### Step 5: Initialize Git Repository (if not done)

```bash
cd /path/to/InternationalFootballEDA

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: DAB setup with CI/CD"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/InternationalFootballEDA.git

# Create main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 6: Create a Develop Branch

```bash
# Create and push develop branch
git checkout -b develop
git push -u origin develop
```

## Workflow Diagram

```
┌─────────────────┐
│  Feature Branch │
└────────┬────────┘
         │
         │ Create PR
         ▼
┌─────────────────────────┐
│   PR Validation         │
│   - Validate bundle     │
│   - Lint notebooks      │
│   - Run unit tests      │
│   - Integration tests   │
└─────────┬───────────────┘
          │
          │ PR Approved & Merged
          ▼
┌─────────────────────────┐
│   Develop Branch        │
│   Auto-deploy to        │
│   STAGING               │
└─────────┬───────────────┘
          │
          │ Merge to Main
          ▼
┌─────────────────────────┐
│   Main Branch           │
│   Auto-deploy to        │
│   PRODUCTION            │
└─────────────────────────┘
```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** to notebooks or bundle config

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "Add new feature"
   git push origin feature/my-new-feature
   ```

4. **Create a Pull Request** to `develop` branch
   * GitHub Actions will automatically validate
   * Review the validation results in the PR comments

5. **After PR approval**, merge to `develop`
   * Automatically deploys to **staging**
   * Monitor the deployment in the Actions tab

6. **Test in staging environment**
   * Verify everything works correctly
   * Run manual tests if needed

7. **Create PR from `develop` to `main`**
   * Requires approval (if protection rules set)
   * Merging deploys to **production**

## Manual Deployment

You can also trigger deployments manually:

1. Go to **Actions** tab
2. Select **Deploy Bundle** workflow
3. Click **Run workflow**
4. Choose environment: dev, staging, or prod
5. Click **Run workflow**

## Monitoring Deployments

### View Workflow Runs
* Go to **Actions** tab in GitHub
* Click on a workflow run to see details
* Check logs for each step

### View Deployed Jobs
* Go to your Databricks workspace
* Navigate to **Workflows** → **Jobs**
* Look for jobs prefixed with `[dev]`, `[staging]`, or `[prod]`

## Troubleshooting

### Workflow fails with authentication error
* Verify `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets are set correctly
* Check token hasn't expired
* Ensure token has sufficient permissions

### Bundle validation fails
* Run locally: `databricks bundle validate --target dev`
* Check YAML syntax in `databricks.yml`
* Verify all notebook paths exist

### Deployment fails
* Check workspace permissions
* Verify catalog names exist for each environment
* Review workflow logs for specific errors

### Jobs not running after deployment
* Check job schedules (some are paused by default)
* Verify cluster configurations
* Check notebook execution history

## Next Steps

1. **Add unit tests** in the `tests/` directory
2. **Create test notebooks** for integration testing
3. **Set up notifications** (Slack, email) for deployment failures
4. **Add code coverage** reporting
5. **Implement data quality tests** in your workflows

## Resources

* [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/)
* [GitHub Actions Documentation](https://docs.github.com/en/actions)
* [Databricks CLI Reference](https://docs.databricks.com/dev-tools/cli/)
