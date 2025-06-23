#!/usr/bin/env python3

import os
from datetime import datetime

def print_environment_info():
    """Print current environment information"""
    environment = os.environ.get('ENVIRONMENT', 'unknown')
    print(f"Environment: {environment.upper()}")
    print(f"GitHub Repository: {os.environ.get('GITHUB_REPOSITORY', 'N/A')}")
    print(f"GitHub Workflow: {os.environ.get('GITHUB_WORKFLOW', 'N/A')}")
    print(f"GitHub Actor: {os.environ.get('GITHUB_ACTOR', 'N/A')}")
    print()

def mask_secret(value, show_chars=6):
    """Mask a secret value showing only first and last few characters"""
    if len(value) <= show_chars * 2:
        return f"{'*' * (len(value) - 4)}{value[-2:]}" if len(value) > 4 else "***"
    
    first_part = value[:show_chars]
    last_part = value[-show_chars:]
    middle_stars = '*' * min(10, len(value) - (show_chars * 2))
    return f"{first_part}{middle_stars}{last_part}"

def print_secrets():
    """Print the three main environment secrets with detailed information"""
    print("=== Environment Secrets (Detailed View) ===")
    
    secrets = {
        'APP_NAME': os.environ.get('APP_NAME'),
        'API_URL': os.environ.get('API_URL'),
        'DATABASE_URL': os.environ.get('DATABASE_URL')
    }
    
    for secret_name, secret_value in secrets.items():
        if secret_value:
            print(f"\n{secret_name}:")
            print(f"  Length: {len(secret_value)} characters")
            
            if secret_name == 'APP_NAME':
                # Show APP_NAME in full as it's not sensitive
                print(f"  Value: {secret_value}")
            elif secret_name == 'API_URL':
                # Show masked URL but reveal domain
                print(f"  Masked: {mask_secret(secret_value)}")
                # Extract and show domain if it's a URL
                if '://' in secret_value:
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(secret_value)
                        print(f"  Domain: {parsed.netloc}")
                        print(f"  Scheme: {parsed.scheme}")
                    except:
                        pass
            elif secret_name == 'DATABASE_URL':
                # Show masked DB URL but reveal database type and host
                print(f"  Masked: {mask_secret(secret_value)}")
                # Extract database info if it's a connection string
                if '://' in secret_value:
                    try:
                        from urllib.parse import urlparse
                        parsed = urlparse(secret_value)
                        print(f"  DB Type: {parsed.scheme}")
                        print(f"  Host: {parsed.hostname}")
                        print(f"  Port: {parsed.port if parsed.port else 'default'}")
                        print(f"  Database: {parsed.path.lstrip('/') if parsed.path else 'N/A'}")
                    except:
                        pass
        else:
            print(f"\n{secret_name}: ❌ NOT SET")
    
    print()

def validate_secrets():
    """Validate that all required secrets are present"""
    print("=== Secret Validation ===")
    
    required_secrets = ['APP_NAME', 'API_URL', 'DATABASE_URL']
    missing_secrets = []
    
    for secret in required_secrets:
        if not os.environ.get(secret):
            missing_secrets.append(secret)
    
    if missing_secrets:
        print(f"❌ Missing secrets: {', '.join(missing_secrets)}")
        return False
    else:
        print("✅ All required secrets are present")
        return True

def print_additional_env_vars():
    """Print additional environment variables that might be useful"""
    print("=== Additional Environment Variables ===")
    
    additional_vars = ['ENVIRONMENT', 'GITHUB_REF', 'GITHUB_SHA', 'RUNNER_OS']
    
    for var in additional_vars:
        value = os.environ.get(var)
        if value:
            print(f"{var}: {value}")
    
    print()

def print_verification_summary():
    """Print a summary for verification purposes"""
    print("=== Verification Summary ===")
    environment = os.environ.get('ENVIRONMENT', 'unknown').upper()
    
    print(f"Environment: {environment}")
    print("Expected secrets for this environment:")
    
    if environment == 'DEVELOPMENT':
        print("  - APP_NAME should contain 'Development'")
        print("  - API_URL should point to dev/development domain")
        print("  - DATABASE_URL should point to dev/development database")
    elif environment == 'PRODUCTION':
        print("  - APP_NAME should contain 'Production'")
        print("  - API_URL should point to production domain")
        print("  - DATABASE_URL should point to production database")
    
    # Check if values match expected pattern
    app_name = os.environ.get('APP_NAME', '')
    api_url = os.environ.get('API_URL', '')
    db_url = os.environ.get('DATABASE_URL', '')
    
    print("\nVerification checks:")
    if environment == 'DEVELOPMENT':
        print(f"  ✅ APP_NAME contains 'Development': {'Development' in app_name}")
        print(f"  ✅ API_URL contains 'dev': {'dev' in api_url.lower()}")
        print(f"  ✅ DATABASE_URL contains 'dev': {'dev' in db_url.lower()}")
    elif environment == 'PRODUCTION':
        print(f"  ✅ APP_NAME contains 'Production': {'Production' in app_name}")
        print(f"  ✅ API_URL is production-like: {not any(env in api_url.lower() for env in ['dev', 'test', 'staging'])}")
        print(f"  ✅ DATABASE_URL is production-like: {not any(env in db_url.lower() for env in ['dev', 'test', 'staging'])}")
    
    print()

def main():
    print("=== GitHub Environment Secrets Reader (Python) ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*55)
    
    # Print environment information
    print_environment_info()
    
    # Print and validate secrets
    print_secrets()
    is_valid = validate_secrets()
    print()
    
    # Print verification summary
    print_verification_summary()
    
    # Print additional environment variables
    print_additional_env_vars()
    
    print("="*55)
    if is_valid:
        print("✅ Script execution completed successfully")
    else:
        print("❌ Script execution completed with issues")
        exit(1)

if __name__ == "__main__":
    main() 