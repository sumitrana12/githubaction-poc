#!/usr/bin/env python3

import os
from datetime import datetime

def handle_env_file(env_name, env_content):
    """Handle environment file secrets by creating .env files and loading variables"""
    env_file = f"{env_name.lower().replace('_env_file', '')}.env"
    
    if env_content:
        print(f"Processing {env_name} environment file...")
        
        # Write content to file
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        # Count lines
        lines = env_content.count('\n') + 1 if env_content.strip() else 0
        print(f"  - Created: {env_file}")
        print(f"  - Lines: {lines}")
        
        # Show preview (mask values)
        preview_lines = env_content.strip().split('\n')[:3]
        print("  - Content preview:")
        for line in preview_lines:
            if '=' in line:
                key, _ = line.split('=', 1)
                print(f"    {key}=***")
            else:
                print(f"    {line}")
        
        # Load variables into environment
        load_env_file(env_file)
        print(f"  - Environment variables loaded from {env_file}")
    else:
        print(f"{env_name}: Not set")
    
    print()

def load_env_file(env_file):
    """Load environment variables from a .env file"""
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error loading {env_file}: {e}")

def print_loaded_variables():
    """Print common environment variables that might be loaded"""
    print("=== Loaded Environment Variables ===")
    common_vars = ['APP_NAME', 'API_URL', 'DATABASE_URL', 'DEBUG', 'PORT', 'NODE_ENV', 'ENVIRONMENT']
    
    for var in common_vars:
        value = os.environ.get(var)
        if value:
            # Mask sensitive-looking values
            if any(keyword in var.upper() for keyword in ['URL', 'KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                print(f"{var}: [PRESENT - {len(value)} characters]")
            else:
                print(f"{var}: {value}")

def main():
    print("=== GitHub Environment Secrets Reader (Python) ===")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Handle environment file secrets
    env_files = {
        'DEV_ENV_FILE': os.environ.get('DEV_ENV_FILE'),
        'PROD_ENV_FILE': os.environ.get('PROD_ENV_FILE'),
        'STAGING_ENV_FILE': os.environ.get('STAGING_ENV_FILE')
    }
    
    for env_name, env_content in env_files.items():
        handle_env_file(env_name, env_content)
    
    # Print loaded variables
    print_loaded_variables()
    
    print("="*50)
    print("All environment variables containing 'ENV', 'KEY', 'SECRET', etc.:")
    
    # List all environment variables (filtered for security)
    env_vars = list(os.environ.keys())
    secret_vars = [var for var in env_vars if any(keyword in var.upper() 
                   for keyword in ['SECRET', 'KEY', 'TOKEN', 'PASSWORD', 'ENV', 'API', 'DATABASE'])]
    
    if secret_vars:
        for var in sorted(secret_vars):
            value = os.environ.get(var, "")
            print(f"  {var}: [PRESENT - {len(value)} characters]")
    else:
        print("No environment variables found")
    
    print("="*50)
    print("Script execution completed")

if __name__ == "__main__":
    main() 