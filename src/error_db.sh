#!/bin/bash
# ============================================================================
# UAFT Error Database Module
# ============================================================================
# Provides fail-safe error logging for LLM reference.
# Logs errors to a JSONL file in ~/.local/share/uaft/error_db.jsonl
# Zero dependencies (no jq required).
# ============================================================================

# Initialize Error DB path
UAFT_DATA_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/uaft"
UAFT_ERROR_DB="${UAFT_DATA_DIR}/error_db.jsonl"

# Ensure directory exists
mkdir -p "$UAFT_DATA_DIR"

# Function to escape JSON strings manually
json_escape() {
    local input="$1"
    # Escape backslashes, quotes, newlines, tabs
    input="${input//\\/\\\\}"
    input="${input//\"/\\\"}"
    input="${input//$'\n'/\\n}"
    input="${input//$'\t'/\\t}"
    echo "$input"
}

# Function to log error
# Usage: log_error_db <exit_code> <command> <error_message>
log_error_db() {
    local exit_code="$1"
    local cmd="$2"
    local msg="${3:-Unknown error}"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # Escape fields
    local esc_cmd
    esc_cmd=$(json_escape "$cmd")
    local esc_msg
    esc_msg=$(json_escape "$msg")
    
    # Construct JSON line
    local json_line="{\"timestamp\": \"$timestamp\", \"exit_code\": $exit_code, \"command\": \"$esc_cmd\", \"error\": \"$esc_msg\", \"context\": \"uaft_cli\"}"
    
    # Append to file silently
    echo "$json_line" >> "$UAFT_ERROR_DB"
    
    # Keep only last 100 lines to prevent infinite growth
    if [[ $(wc -l < "$UAFT_ERROR_DB") -gt 100 ]]; then
        local temp_file="${UAFT_ERROR_DB}.tmp"
        tail -n 100 "$UAFT_ERROR_DB" > "$temp_file"
        mv "$temp_file" "$UAFT_ERROR_DB"
    fi

    # Try to log to global Failsafe DB if available
    if command -v fsdb >/dev/null 2>&1; then
        fsdb log --tool "uaft" --error "$msg" --context "$cmd" --severity "error" >/dev/null 2>&1 || true
    fi
}

# Trap handler
handle_error_trap() {
    local exit_code=$?
    local cmd="$BASH_COMMAND"
    
    # Don't log if exit code is 0 (success)
    if [[ $exit_code -eq 0 ]]; then
        return
    fi
    
    # Log the error
    log_error_db "$exit_code" "$cmd" "Command failed with exit code $exit_code"
    
    # We do NOT print to user, as requested ("user shouldn't see any processes")
    # The script will exit naturally due to set -e or continue if handled
}

# Export functions
export -f log_error_db
export -f json_escape
