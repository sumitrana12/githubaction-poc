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

def print_secrets():
    """Print the three main environment secrets"""
    print("=== Environment Secrets ===")
    
    secrets = {
        'APP_NAME': os.environ.get('APP_NAME'),
        'API_URL': os.environ.get('API_URL'),
        'DATABASE_URL': os.environ.get('DATABASE_URL')
    }
    
    for secret_name, secret_value in secrets.items():
        if secret_value:
            # Mask sensitive-looking values (URLs and DATABASE_URL)
            if secret_name in ['API_URL', 'DATABASE_URL']:
                print(f"{secret_name}: [PRESENT - {len(secret_value)} characters]")
            else:
                print(f"{secret_name}: {secret_value}")
        else:
            print(f"{secret_name}: NOT SET")
    
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