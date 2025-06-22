#!/bin/bash

# Script to print GitHub secrets and handle environment files
# Secrets are passed as environment variables in GitHub Actions

echo "=== GitHub Environment Secrets Reader ==="
echo "Date: $(date)"
echo "============================================"

# Function to handle environment file secrets
handle_env_file() {
    local env_name=$1
    local env_content=$2
    local env_file="${env_name,,}.env"  # Convert to lowercase for filename
    
    if [ ! -z "$env_content" ]; then
        echo "Processing $env_name environment file..."
        echo "$env_content" > "$env_file"
        echo "  - Created: $env_file"
        echo "  - Lines: $(wc -l < "$env_file")"
        echo "  - Content preview:"
        echo "    $(head -3 "$env_file" | sed 's/=.*/=***/')"
        
        # Source the environment file to make variables available
        set -a  # automatically export all variables
        source "$env_file"
        set +a  # turn off automatic export
        
        echo "  - Environment variables loaded from $env_file"
    else
        echo "$env_name: Not set"
    fi
    echo ""
}

# Handle environment file secrets
handle_env_file "DEV_ENV_FILE" "$DEV_ENV_FILE"
handle_env_file "PROD_ENV_FILE" "$PROD_ENV_FILE"
handle_env_file "STAGING_ENV_FILE" "$STAGING_ENV_FILE"

# Print some common environment variables that might be loaded
echo "=== Loaded Environment Variables ==="
for var in APP_NAME API_URL DATABASE_URL DEBUG PORT; do
    if [ ! -z "${!var}" ]; then
        if [[ "$var" == *"URL"* ]] || [[ "$var" == *"KEY"* ]] || [[ "$var" == *"SECRET"* ]]; then
            echo "$var: [PRESENT - ${#!var} characters]"
        else
            echo "$var: ${!var}"
        fi
    fi
done

echo "============================================"
echo "Script execution completed" 