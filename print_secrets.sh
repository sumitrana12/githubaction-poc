#!/bin/bash

# Script to print GitHub environment secrets
# Works with individual environment secrets: APP_NAME, API_URL, DATABASE_URL

echo "=== GitHub Environment Secrets Reader (Shell) ==="
echo "Date: $(date)"
echo "=================================================="

# Function to mask a secret value showing first and last characters
mask_secret() {
    local value="$1"
    local show_chars=6
    local len=${#value}
    
    if [ $len -le $((show_chars * 2)) ]; then
        if [ $len -gt 4 ]; then
            echo "${value:0:2}$(printf '*%.0s' {1..6})${value: -2}"
        else
            echo "***"
        fi
    else
        local first_part="${value:0:$show_chars}"
        local last_part="${value: -$show_chars}"
        printf "%s**********%s" "$first_part" "$last_part"
    fi
}

# Function to extract domain from URL
extract_url_info() {
    local url="$1"
    if [[ "$url" == *"://"* ]]; then
        # Extract protocol
        local protocol="${url%%://*}"
        # Extract domain (remove protocol and path)
        local domain_path="${url#*://}"
        local domain="${domain_path%%/*}"
        # Extract host (remove port if present)
        local host="${domain%%:*}"
        # Extract port if present
        local port="${domain#*:}"
        if [ "$port" = "$domain" ]; then
            port="default"
        fi
        
        echo "    Protocol: $protocol"
        echo "    Host: $host"
        echo "    Port: $port"
    fi
}

# Function to extract database info from DATABASE_URL
extract_db_info() {
    local db_url="$1"
    if [[ "$db_url" == *"://"* ]]; then
        # Extract database type
        local db_type="${db_url%%://*}"
        # Extract the rest
        local rest="${db_url#*://}"
        # Extract user info (before @)
        local userinfo="${rest%%@*}"
        # Extract host and database (after @)
        local hostdb="${rest#*@}"
        # Extract host:port (before /)
        local hostport="${hostdb%%/*}"
        # Extract database name (after /)
        local database="${hostdb#*/}"
        # Extract host (before :)
        local host="${hostport%%:*}"
        # Extract port (after :)
        local port="${hostport#*:}"
        if [ "$port" = "$hostport" ]; then
            port="default"
        fi
        
        echo "    DB Type: $db_type"
        echo "    Host: $host"
        echo "    Port: $port"
        echo "    Database: $database"
    fi
}

# Function to print environment information
print_environment_info() {
    echo "=== Environment Information ==="
    echo "Environment: ${ENVIRONMENT:-unknown}"
    echo "GitHub Repository: ${GITHUB_REPOSITORY:-N/A}"
    echo "GitHub Workflow: ${GITHUB_WORKFLOW:-N/A}"
    echo "GitHub Actor: ${GITHUB_ACTOR:-N/A}"
    echo ""
}

# Function to print secrets with detailed information
print_secrets() {
    echo "=== Environment Secrets (Detailed View) ==="
    
    # Define the three main secrets
    declare -a secrets=("APP_NAME" "API_URL" "DATABASE_URL")
    
    for secret in "${secrets[@]}"; do
        value="${!secret}"
        if [ ! -z "$value" ]; then
            echo ""
            echo "$secret:"
            echo "  Length: ${#value} characters"
            
            case "$secret" in
                "APP_NAME")
                    # Show APP_NAME in full as it's not sensitive
                    echo "  Value: $value"
                    ;;
                "API_URL")
                    # Show masked URL but reveal domain info
                    echo "  Masked: $(mask_secret "$value")"
                    extract_url_info "$value"
                    ;;
                "DATABASE_URL")
                    # Show masked DB URL but reveal database info
                    echo "  Masked: $(mask_secret "$value")"
                    extract_db_info "$value"
                    ;;
            esac
        else
            echo ""
            echo "$secret: ❌ NOT SET"
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

# Function to print verification summary
print_verification_summary() {
    echo "=== Verification Summary ==="
    local environment="${ENVIRONMENT:-unknown}"
    environment=$(echo "$environment" | tr '[:lower:]' '[:upper:]')
    
    echo "Environment: $environment"
    echo "Expected secrets for this environment:"
    
    case "$environment" in
        "DEVELOPMENT")
            echo "  - APP_NAME should contain 'Development'"
            echo "  - API_URL should point to dev/development domain"
            echo "  - DATABASE_URL should point to dev/development database"
            ;;
        "PRODUCTION")
            echo "  - APP_NAME should contain 'Production'"
            echo "  - API_URL should point to production domain"
            echo "  - DATABASE_URL should point to production database"
            ;;
    esac
    
    # Check if values match expected pattern
    echo ""
    echo "Verification checks:"
    
    case "$environment" in
        "DEVELOPMENT")
            if [[ "$APP_NAME" == *"Development"* ]]; then
                echo "  ✅ APP_NAME contains 'Development': true"
            else
                echo "  ❌ APP_NAME contains 'Development': false"
            fi
            
            if [[ "${API_URL,,}" == *"dev"* ]]; then
                echo "  ✅ API_URL contains 'dev': true"
            else
                echo "  ❌ API_URL contains 'dev': false"
            fi
            
            if [[ "${DATABASE_URL,,}" == *"dev"* ]]; then
                echo "  ✅ DATABASE_URL contains 'dev': true"
            else
                echo "  ❌ DATABASE_URL contains 'dev': false"
            fi
            ;;
        "PRODUCTION")
            if [[ "$APP_NAME" == *"Production"* ]]; then
                echo "  ✅ APP_NAME contains 'Production': true"
            else
                echo "  ❌ APP_NAME contains 'Production': false"
            fi
            
            if [[ "${API_URL,,}" != *"dev"* && "${API_URL,,}" != *"test"* && "${API_URL,,}" != *"staging"* ]]; then
                echo "  ✅ API_URL is production-like: true"
            else
                echo "  ❌ API_URL is production-like: false"
            fi
            
            if [[ "${DATABASE_URL,,}" != *"dev"* && "${DATABASE_URL,,}" != *"test"* && "${DATABASE_URL,,}" != *"staging"* ]]; then
                echo "  ✅ DATABASE_URL is production-like: true"
            else
                echo "  ❌ DATABASE_URL is production-like: false"
            fi
            ;;
    esac
    echo ""
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
    print_verification_summary
    print_additional_env_vars
    echo "=================================================="
    echo "✅ Script execution completed successfully"
    exit 0
else
    echo ""
    print_verification_summary
    print_additional_env_vars
    echo "=================================================="
    echo "❌ Script execution completed with issues"
    exit 1
fi 