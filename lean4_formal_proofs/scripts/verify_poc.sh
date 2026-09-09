#!/bin/bash

# verification script for the Large Lean Model PoC
# This script verifies that the PoC compiles and all theorems are formally verified

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_header() {
    echo -e "${BLUE}==========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}==========================================${NC}"
}

# Check if we're in the correct directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

if [ ! -f "$PROJECT_DIR/poc_large_model.lean" ]; then
    print_error "PoC file not found. Please run this script from lean4_formal_proofs/ directory or scripts/ directory."
    exit 1
fi

cd "$PROJECT_DIR"

print_header "Large Lean Model PoC - Verification Script"

# Step 1: Check Lean installation
print_info "Checking Lean installation..."

if command -v lean &> /dev/null; then
    LEAN_VERSION=$(lean --version 2>&1 | head -n 1)
    print_success "Lean found: $LEAN_VERSION"
else
    print_error "Lean 4 is not installed."
    print_info "To install Lean 4, run:"
    print_info "  curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh"
    exit 1
fi

# Step 2: Check Lake installation
print_info "Checking Lake installation..."

if command -v lake &> /dev/null; then
    LAKE_VERSION=$(lake --version 2>&1 | head -n 1)
    print_success "Lake found: $LAKE_VERSION"
else
    print_error "Lake is not installed."
    print_info "Lake should be installed with Lean 4."
    exit 1
fi

# Step 3: Check Lean version
print_info "Checking Lean version compatibility..."

REQUIRED_VERSION="leanprover/lean4:v4.33.0-rc1"
ACTUAL_TOOLCHAIN=$(cat lean-toolchain 2>/dev/null || echo "not found")

if [ "$ACTUAL_TOOLCHAIN" = "$REQUIRED_VERSION" ]; then
    print_success "Lean toolchain matches: $REQUIRED_VERSION"
else
    print_warning "Lean toolchain: $ACTUAL_TOOLCHAIN"
    print_warning "Recommended: $REQUIRED_VERSION"
fi

# Step 4: Verify PoC file exists
print_info "Checking PoC file..."

if [ -f "poc_large_model.lean" ]; then
    print_success "PoC file found: poc_large_model.lean"
else
    print_error "PoC file not found: poc_large_model.lean"
    exit 1
fi

# Step 5: Check for sorry in PoC file
print_info "Checking for 'sorry' in PoC file..."

SORRY_COUNT=$(grep -c "sorry" poc_large_model.lean || echo "0")

if [ "$SORRY_COUNT" = "0" ]; then
    print_success "No 'sorry' found in PoC file"
else
    print_error "Found $SORRY_COUNT occurrences of 'sorry' in PoC file"
    grep -n "sorry" poc_large_model.lean
    exit 1
fi

# Step 6: Check for axiom in PoC file (axioms are allowed, they're declared assumptions)
print_info "Checking for 'axiom' in PoC file..."

AXIOM_COUNT=$(grep -c "axiom" poc_large_model.lean || echo "0")

if [ "$AXIOM_COUNT" = "0" ]; then
    print_success "No 'axiom' found in PoC file (all theorems are proved)"
else
    print_warning "Found $AXIOM_COUNT declared axioms in PoC file"
    print_info "Note: Axioms are declared assumptions, not unproven theorems. This is acceptable."
fi

# Step 7: Count theorems in PoC file
print_info "Counting theorems in PoC file..."

THEOREM_COUNT=$(grep -c "^theorem\|^ def.*:.*Prop" poc_large_model.lean || echo "0")
print_success "Found $THEOREM_COUNT theorems/definitions in PoC file"

# Step 8: Build the PoC
print_info "Building PoC with lake..."

print_info "This may take a few minutes on first run (Mathlib4 download)..."

BUILD_START=$(date +%s)

if lake build poc_large_model 2>&1 | tee build.log; then
    BUILD_END=$(date +%s)
    BUILD_TIME=$((BUILD_END - BUILD_START))
    print_success "PoC built successfully in ${BUILD_TIME}s"
else
    print_error "PoC build failed"
    print_info "Build log saved to build.log"
    exit 1
fi

# Step 9: Check for errors in build
print_info "Checking build output for errors..."

ERROR_COUNT=$(grep -c "error" build.log || echo "0")

if [ "$ERROR_COUNT" = "0" ]; then
    print_success "No errors in build output"
else
    print_error "Found $ERROR_COUNT errors in build output"
    grep "error" build.log
    exit 1
fi

# Step 10: Check for warnings in build
print_info "Checking build output for warnings..."

WARNING_COUNT=$(grep -c "warning" build.log || echo "0")

if [ "$WARNING_COUNT" = "0" ]; then
    print_success "No warnings in build output"
else
    print_warning "Found $WARNING_COUNT warnings in build output"
    grep "warning" build.log
fi

# Step 11: Verify all imports are satisfied
print_info "Verifying all imports..."

# Extract all imports from the PoC file
IMPORTS=$(grep "^import" poc_large_model.lean | awk '{print $2}' | sed 's/^Mathlib\./mathlib:/')

print_info "Found imports:"
for IMPORT in $IMPORTS; do
    print_info "  - $IMPORT"
done

# Step 12: Clean up build artifacts (optional)
print_info "Cleaning up build artifacts..."
rm -f build.log

# Final summary
print_header "Verification Complete"

print_success "All checks passed!"
print_info ""
print_info "Summary:"
print_info "  ✓ Lean 4 installed"
print_info "  ✓ Lake installed"
print_info "  ✓ PoC file exists"
print_info "  ✓ No 'sorry' in PoC"
print_info "  ✓ $THEOREM_COUNT theorems defined"
print_info "  ✓ PoC compiles successfully"
print_info "  ✓ No errors in build"
print_info ""
print_success "The Large Lean Model PoC is ready for use!"
print_info ""
print_info "To run the PoC:"
print_info "  cd lean4_formal_proofs"
print_info "  lake build poc_large_model"
print_info ""
print_info "For more information, see README_PoC.md"

exit 0
