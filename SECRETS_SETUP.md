# GitHub Secrets Setup Guide

This guide explains how to set up the three GitHub secrets (`DEV_ENV_FILE`, `PROD_ENV_FILE`, and `STAGING_ENV_FILE`) that contain multiple environment variables.

## Setting up GitHub Secrets

1. Go to your repository on GitHub
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Create the following three secrets:

### DEV_ENV_FILE
**Secret Name:** `DEV_ENV_FILE`
**Secret Value:**
```
APP_NAME=MyApp Development
API_URL=https://dev-api.example.com
DATABASE_URL=postgresql://devuser:devpass@dev-db.example.com:5432/myapp_dev
DEBUG=true
PORT=3000
NODE_ENV=development
JWT_SECRET=dev-jwt-secret-key-123
REDIS_URL=redis://dev-redis.example.com:6379
LOG_LEVEL=debug
CORS_ORIGIN=http://localhost:3000,http://localhost:3001
```

### STAGING_ENV_FILE
**Secret Name:** `STAGING_ENV_FILE`
**Secret Value:**
```
APP_NAME=MyApp Staging
API_URL=https://staging-api.example.com
DATABASE_URL=postgresql://staginguser:stagingpass@staging-db.example.com:5432/myapp_staging
DEBUG=false
PORT=3000
NODE_ENV=staging
JWT_SECRET=staging-jwt-secret-key-456
REDIS_URL=redis://staging-redis.example.com:6379
LOG_LEVEL=info
CORS_ORIGIN=https://staging.example.com
EMAIL_SERVICE=staging-email-service
```

### PROD_ENV_FILE
**Secret Name:** `PROD_ENV_FILE`
**Secret Value:**
```
APP_NAME=MyApp Production
API_URL=https://api.example.com
DATABASE_URL=postgresql://produser:prodpass@prod-db.example.com:5432/myapp
DEBUG=false
PORT=80
NODE_ENV=production
JWT_SECRET=super-secure-production-jwt-key-789
REDIS_URL=redis://prod-redis.example.com:6379
LOG_LEVEL=warn
CORS_ORIGIN=https://example.com
EMAIL_SERVICE=production-email-service
MONITORING_API_KEY=prod-monitoring-key-xyz
CDN_URL=https://cdn.example.com
```

## Using in GitHub Actions

The workflow file (`.github/workflows/test-secrets.yml`) demonstrates three approaches:

### 1. Environment-Specific Jobs
```yaml
test-dev-environment:
  runs-on: ubuntu-latest
  environment: development  # Uses GitHub Environments
  steps:
    - name: Test Development Environment
      env:
        DEV_ENV_FILE: ${{ secrets.DEV_ENV_FILE }}
        STAGING_ENV_FILE: ${{ secrets.STAGING_ENV_FILE }}
      run: ./print_secrets.sh
```

### 2. Production Job
```yaml
test-prod-environment:
  runs-on: ubuntu-latest
  environment: production  # Uses GitHub Environments
  steps:
    - name: Test Production Environment
      env:
        PROD_ENV_FILE: ${{ secrets.PROD_ENV_FILE }}
      run: ./print_secrets.sh
```

### 3. Demo with Inline Values
Shows how the secrets work with sample data for testing.

## How the Scripts Work

Both `print_secrets.sh` and `print_secrets.py` will:

1. **Create .env files**: Each environment secret creates a corresponding `.env` file
   - `DEV_ENV_FILE` → `dev.env`
   - `STAGING_ENV_FILE` → `staging.env`
   - `PROD_ENV_FILE` → `prod.env`

2. **Load variables**: All variables from the .env files are loaded into the environment

3. **Display safely**: Show which variables are loaded while masking sensitive values

## Security Best Practices

- **Never commit .env files** to your repository
- **Use different secrets** for each environment
- **Rotate secrets regularly**
- **Use GitHub Environments** for additional protection of production secrets
- **Limit access** to production secrets to specific team members

## Testing Locally

You can test the scripts locally by creating environment files:

```bash
# Create a test environment file
echo "APP_NAME=Local Test
API_URL=http://localhost:8000
DEBUG=true" > test.env

# Export the content as an environment variable
export DEV_ENV_FILE="$(cat test.env)"

# Run the scripts
./print_secrets.sh
python3 print_secrets.py
```

## Common Use Cases

- **Multi-environment deployments** (dev, staging, production)
- **Feature branch testing** with development environment
- **Configuration management** across different stages
- **Secret management** for microservices
- **Database connection strings** per environment
- **API keys and tokens** specific to each environment 