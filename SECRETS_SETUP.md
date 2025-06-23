# GitHub Environment Secrets Setup Guide

This guide explains how to set up GitHub environment secrets for your repository with two environments (development and production) and three secrets per environment.

## Environment Structure

- **Environments**: `development` and `production`
- **Secrets per environment**: `APP_NAME`, `API_URL`, and `DATABASE_URL`

## Setting up GitHub Environments and Secrets

### Step 1: Create Environments

1. Go to your repository on GitHub
2. Click on **Settings** → **Environments**
3. Click **New environment**
4. Create two environments:
   - `development`
   - `production`

### Step 2: Add Secrets to Each Environment

For each environment, add the following three secrets:

#### Development Environment Secrets

Navigate to the `development` environment and add these secrets:

**Secret Name:** `APP_NAME`
**Secret Value:** `MyApp Development`

**Secret Name:** `API_URL`
**Secret Value:** `https://dev-api.example.com`

**Secret Name:** `DATABASE_URL`
**Secret Value:** `postgresql://devuser:devpass@dev-db.example.com:5432/myapp_dev`

#### Production Environment Secrets

Navigate to the `production` environment and add these secrets:

**Secret Name:** `APP_NAME`
**Secret Value:** `MyApp Production`

**Secret Name:** `API_URL`
**Secret Value:** `https://api.example.com`

**Secret Name:** `DATABASE_URL`
**Secret Value:** `postgresql://produser:prodpass@prod-db.example.com:5432/myapp`

## How GitHub Actions Uses These Secrets

The workflow file (`.github/workflows/test-secrets.yml`) demonstrates how to use environment-specific secrets:

### Development Job
```yaml
test-development-environment:
  runs-on: ubuntu-latest
  environment: development  # Uses development environment
  steps:
    - name: Test Development Environment
      env:
        APP_NAME: ${{ secrets.APP_NAME }}
        API_URL: ${{ secrets.API_URL }}
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        ENVIRONMENT: development
      run: |
        ./print_secrets.sh
        python3 print_secrets.py
```

### Production Job
```yaml
test-production-environment:
  runs-on: ubuntu-latest
  environment: production  # Uses production environment
  steps:
    - name: Test Production Environment
      env:
        APP_NAME: ${{ secrets.APP_NAME }}
        API_URL: ${{ secrets.API_URL }}
        DATABASE_URL: ${{ secrets.DATABASE_URL }}
        ENVIRONMENT: production
      run: |
        ./print_secrets.sh
        python3 print_secrets.py
```

## How the Scripts Work

Both `print_secrets.sh` and `print_secrets.py` will:

1. **Print environment information**: Shows which environment is currently running
2. **Display secrets**: Shows the three main secrets (masking sensitive URLs)
3. **Validate secrets**: Ensures all required secrets are present
4. **Show additional variables**: Displays GitHub-specific environment variables

### Sample Output

```
=== GitHub Environment Secrets Reader ===
Date: 2024-01-15 10:30:45
==================================================

=== Environment Information ===
Environment: DEVELOPMENT
GitHub Repository: username/repo-name
GitHub Workflow: Test Environment Secrets
GitHub Actor: username

=== Environment Secrets ===
APP_NAME: MyApp Development
API_URL: [PRESENT - 28 characters]
DATABASE_URL: [PRESENT - 65 characters]

=== Secret Validation ===
✅ All required secrets are present

=== Additional Environment Variables ===
ENVIRONMENT: development
GITHUB_REF: refs/heads/main
GITHUB_SHA: abc123...
RUNNER_OS: Linux

==================================================
✅ Script execution completed successfully
```

## Security Best Practices

- **Use GitHub Environments**: Provides additional protection and allows for environment-specific approval requirements
- **Separate environments**: Keep development and production secrets completely separate
- **Rotate secrets regularly**: Update your secrets periodically for security
- **Limit access**: Use environment protection rules to limit who can deploy to production
- **Monitor usage**: Review GitHub Actions logs to ensure secrets are being used correctly

## Environment Protection Rules (Recommended)

For the production environment, consider adding protection rules:

1. Go to **Settings** → **Environments** → **production**
2. Enable **Required reviewers** to require manual approval for production deployments
3. Add **Deployment branches** rule to only allow deployments from main/master branch
4. Set **Environment secrets** to be accessible only to the production environment

## Testing Locally

You can test the scripts locally by setting environment variables:

```bash
# Set the environment variables
export APP_NAME="Local Test App"
export API_URL="http://localhost:8000"
export DATABASE_URL="postgresql://localhost/testdb"
export ENVIRONMENT="local"

# Run the scripts
./print_secrets.sh
python3 print_secrets.py
```

## Common Use Cases

- **Multi-environment deployments**: Automatic deployment to development, manual approval for production
- **Configuration management**: Different API endpoints and database connections per environment
- **Feature testing**: Safe testing in development environment before production release
- **Database migrations**: Different database connections for each environment
- **API integration**: Environment-specific API keys and endpoints

## Troubleshooting

### Missing Secrets Error
If you see "❌ Missing secrets", ensure:
1. The environment exists in GitHub
2. All three secrets (`APP_NAME`, `API_URL`, `DATABASE_URL`) are added to the environment
3. The job is using the correct environment name in the workflow file

### Access Denied
If the workflow can't access secrets:
1. Check that the repository has the correct permissions
2. Verify the environment protection rules aren't blocking access
3. Ensure the workflow is triggered by an authorized user/event 