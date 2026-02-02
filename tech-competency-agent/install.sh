#!/bin/bash

# Installation script for Technical Competency Extraction Agent System
# This script automates the complete setup process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "\n${BLUE}================================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

print_header "Technical Competency Extraction Agent System - Installation"

# Step 1: Check Python version
print_info "Checking Python version..."
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        print_success "Python $PYTHON_VERSION found (3.11+ required)"
    else
        print_error "Python $PYTHON_VERSION found, but 3.11+ required"
        exit 1
    fi
else
    print_error "Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Step 2: Check for package manager
print_info "Checking for package manager..."
USE_POETRY=false
if command_exists poetry; then
    print_success "Poetry found - will use Poetry for installation"
    USE_POETRY=true
elif command_exists pip3; then
    print_success "pip found - will use pip for installation"
else
    print_error "Neither Poetry nor pip found. Please install one of them."
    exit 1
fi

# Step 3: Install dependencies
print_header "Installing Dependencies"

if [ "$USE_POETRY" = true ]; then
    print_info "Installing dependencies with Poetry..."
    poetry install
    print_success "Dependencies installed with Poetry"
else
    print_info "Installing dependencies with pip..."
    pip3 install -e .
    print_success "Dependencies installed with pip"
fi

# Step 4: Set up environment
print_header "Setting Up Environment"

if [ ! -f .env ]; then
    print_info "Creating .env file from template..."
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please add your ANTHROPIC_API_KEY to .env file"
else
    print_info ".env file already exists"
fi

# Step 5: Generate configuration files
print_header "Generating Configuration Files"

if [ -f "config/workflow_config.yaml" ]; then
    print_info "Configuration files already exist"
else
    print_info "Generating default configuration..."
    if [ "$USE_POETRY" = true ]; then
        poetry run techcomp init-config
    else
        techcomp init-config
    fi
    print_success "Configuration files generated"
fi

# Step 6: Create directory structure
print_header "Creating Directory Structure"

mkdir -p data/input data/output data/knowledge_base
print_success "Directory structure created"

# Step 7: Generate sample data
print_header "Generating Sample Data"

if [ -f "data/input/sample_jobs.xlsx" ]; then
    print_info "Sample data already exists"
else
    print_info "Generating sample data files..."
    python3 data/input/create_sample_data.py
    print_success "Sample data generated"
fi

# Step 8: Run verification
print_header "Verifying Installation"

python3 verify_setup.py
VERIFY_RESULT=$?

if [ $VERIFY_RESULT -eq 0 ]; then
    print_header "Installation Complete!"

    echo -e "${GREEN}✅ All components installed successfully!${NC}\n"

    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. Add your Anthropic API key to .env:"
    echo -e "     ${YELLOW}echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' >> .env${NC}"
    echo -e ""
    echo -e "  2. Test the system:"
    echo -e "     ${YELLOW}python3 test_e2e.py${NC}"
    echo -e ""
    echo -e "  3. Run the workflow with sample data:"
    if [ "$USE_POETRY" = true ]; then
        echo -e "     ${YELLOW}poetry run techcomp run \\${NC}"
    else
        echo -e "     ${YELLOW}techcomp run \\${NC}"
    fi
    echo -e "       ${YELLOW}--jobs-file data/input/sample_jobs.xlsx \\${NC}"
    echo -e "       ${YELLOW}--tech-sources data/input/sample_tech_competencies.xlsx \\${NC}"
    echo -e "       ${YELLOW}--leadership-file data/input/sample_leadership.xlsx \\${NC}"
    echo -e "       ${YELLOW}--template-file data/input/sample_template.xlsx${NC}"
    echo -e ""
    echo -e "  4. See ${BLUE}QUICKSTART.md${NC} for detailed usage"
    echo -e ""
else
    print_warning "Installation completed with warnings"
    echo -e "\n${YELLOW}Please review the verification output above and fix any issues.${NC}"
    exit 1
fi
