#!/bin/bash

# Script to print GitHub environment secrets
# Works with individual environment secrets: APP_NAME, API_URL, DATABASE_URL

echo "=== GitHub Environment Secrets Reader (Shell) ==="
echo "Date: $(date)"
echo "=================================================="

# Function to print environment information
print_environment_info() {
    echo "=== Environment Information ==="
    echo "Environment: ${ENVIRONMENT:-unknown}"
    echo "GitHub Repository: ${GITHUB_REPOSITORY:-N/A}"
    echo "GitHub Workflow: ${GITHUB_WORKFLOW:-N/A}"
    echo "GitHub Actor: ${GITHUB_ACTOR:-N/A}"
    echo ""
}

# Function to print secrets with appropriate masking
print_secrets() {
    echo "=== Environment Secrets ==="
    
    # Define the three main secrets
    declare -a secrets=("APP_NAME" "API_URL" "DATABASE_URL")
    
    for secret in "${secrets[@]}"; do
        value="${!secret}"
        if [ ! -z "$value" ]; then
            # Mask sensitive URLs and database connections
            if [[ "$secret" == *"URL"* ]]; then
                echo "$secret: [PRESENT - ${#value} characters]"
            else
                echo "$secret: $value"
            fi
        else
            echo "$secret: NOT SET"
        fi
    done
    echo ""
}

# Function to validate all required secrets are present
validate_secrets() {
    echo "=== Secret Validation ==="
    
    declare -a required_secrets=("APP_NAME" "API_URL" "DATABASE_URL")
    declare -a missing_secrets=()
    
    for secret in "${required_secrets[@]}"; do
        if [ -z "${!secret}" ]; then
            missing_secrets+=("$secret")
        fi
    done
    
    if [ ${#missing_secrets[@]} -gt 0 ]; then
        echo "❌ Missing secrets: $(IFS=', '; echo "${missing_secrets[*]}")"
        return 1
    else
        echo "✅ All required secrets are present"
        return 0
    fi
}

# Function to print additional environment variables
print_additional_env_vars() {
    echo "=== Additional Environment Variables ==="
    
    declare -a additional_vars=("ENVIRONMENT" "GITHUB_REF" "GITHUB_SHA" "RUNNER_OS")
    
    for var in "${additional_vars[@]}"; do
        value="${!var}"
        if [ ! -z "$value" ]; then
            echo "$var: $value"
        fi
    done
    echo ""
}

# Main execution
print_environment_info
print_secrets

if validate_secrets; then
    echo ""
    print_additional_env_vars
    echo "=================================================="
    echo "✅ Script execution completed successfully"
    exit 0
else
    echo ""
    print_additional_env_vars
    echo "=================================================="
    echo "❌ Script execution completed with issues"
    exit 1
fi 