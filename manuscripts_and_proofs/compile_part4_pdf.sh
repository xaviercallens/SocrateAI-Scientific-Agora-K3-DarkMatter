#!/bin/bash

# Script to compile Part IV LaTeX documents to PDF
# Usage: ./compile_part4_pdf.sh [document_name]
# If no document name is provided, compiles all Part IV documents

set -e  # Exit on error

# Function to display colored messages
function success() {
    echo -e "\033[1;32m✅ $1\033[0m"
}

function info() {
    echo -e "\033[1;34m📄 $1\033[0m"
}

function warning() {
    echo -e "\033[1;33m⚠️  $1\033[0m"
}

function error() {
    echo -e "\033[1;31m❌ $1\033[0m"
}

# Check if we're in the right directory
if [ ! -f "Part_IV_Complete_With_Lean_Proofs.tex" ] && [ ! -f "Part_IV_Rigorous_Resolution_FDM_Tension.tex" ]; then
    error "Part IV LaTeX documents not found"
    echo "Please run this script from manuscripts_and_proofs/ directory"
    exit 1
fi

# Determine which documents to compile
DOCUMENTS=()
if [ $# -eq 0 ]; then
    # Compile all Part IV documents
    if [ -f "Part_IV_Complete_With_Lean_Proofs.tex" ]; then
        DOCUMENTS+=("Part_IV_Complete_With_Lean_Proofs")
    fi
    if [ -f "Part_IV_Rigorous_Resolution_FDM_Tension.tex" ]; then
        DOCUMENTS+=("Part_IV_Rigorous_Resolution_FDM_Tension")
    fi
else
    # Compile specific document
    DOCUMENTS+=("$1")
fi

if [ ${#DOCUMENTS[@]} -eq 0 ]; then
    error "No documents to compile"
    exit 1
fi

info "Starting PDF compilation for ${#DOCUMENTS[@]} document(s)..."

# Check for LaTeX compilers
COMPILER=""
if command -v pdflatex &> /dev/null; then
    COMPILER="pdflatex"
elif command -v xelatex &> /dev/null; then
    COMPILER="xelatex"
elif command -v lualatex &> /dev/null; then
    COMPILER="lualatex"
else
    error "No LaTeX compiler found (pdflatex, xelatex, or lualatex)"
    echo ""
    echo "Installation options:"
    echo "1. Install TeX Live: sudo apt-get install texlive texlive-latex-extra"
    echo "2. Use Docker: docker run -it --rm -v \$(pwd):/workdir texlive/texlive:latest"
    echo "3. Use Overleaf: Upload to https://www.overleaf.com/"
    exit 1
fi

success "Found LaTeX compiler: $COMPILER"

# Function to compile a single document
compile_document() {
    local doc_name=$1
    local tex_file="${doc_name}.tex"
    local pdf_file="${doc_name}.pdf"
    
    info "Compiling $tex_file..."
    
    # First pass
    if ! $COMPILER -interaction=nonstopmode "$tex_file" > /dev/null 2>&1; then
        warning "First pass had issues, continuing..."
    fi
    
    # Second pass (for references)
    if ! $COMPILER -interaction=nonstopmode "$tex_file" > /dev/null 2>&1; then
        warning "Second pass had issues, continuing..."
    fi
    
    # Third pass (final)
    if ! $COMPILER -interaction=nonstopmode "$tex_file" > /dev/null 2>&1; then
        warning "Third pass had issues, but continuing..."
    fi
    
    # Check if PDF was created
    if [ -f "$pdf_file" ]; then
        local size=$(du -h "$pdf_file" | cut -f1)
        local pages="unknown"
        
        # Try to get page count
        if command -v pdfinfo &> /dev/null; then
            pages=$(pdfinfo "$pdf_file" | grep Pages | awk '{print $2}')
        fi
        
        success "$pdf_file generated successfully"
        echo "   Size: $size"
        echo "   Pages: $pages"
        return 0
    else
        error "$pdf_file was not created"
        return 1
    fi
}

# Compile all requested documents
SUCCESS_COUNT=0
FAILURE_COUNT=0

for doc in "${DOCUMENTS[@]}"; do
    if compile_document "$doc"; then
        ((SUCCESS_COUNT++))
    else
        ((FAILURE_COUNT++))
    fi
done

echo ""

# Clean up auxiliary files
info "Cleaning up auxiliary files..."
for doc in "${DOCUMENTS[@]}"; do
    rm -f "${doc}.aux" "${doc}.log" "${doc}.out" "${doc}.toc" "${doc}.bbl" "${doc}.blg" 2>/dev/null || true
done

# Generate compilation report
echo ""
info "Generating compilation report..."
REPORT_FILE="compilation_report_$(date +%Y%m%d_%H%M%S).txt"

{
    echo "Part IV PDF Compilation Report"
    echo "=============================="
    echo "Generated: $(date)"
    echo "Compiler: $COMPILER"
    echo ""
    echo "Compilation Results:"
    echo "-------------------"
    
    for doc in "${DOCUMENTS[@]}"; do
        pdf_file="${doc}.pdf"
        if [ -f "$pdf_file" ]; then
            size=$(du -h "$pdf_file" | cut -f1)
            echo "✅ $pdf_file: $size"
        else
            echo "❌ $pdf_file: FAILED"
        fi
    done
    
    echo ""
    echo "Summary:"
    echo "--------"
    echo "Successful: $SUCCESS_COUNT"
    echo "Failed: $FAILURE_COUNT"
    
    if [ $FAILURE_COUNT -eq 0 ]; then
        echo ""
        echo "🎉 All documents compiled successfully!"
    else
        echo ""
        echo "⚠️  Some documents failed to compile"
    fi
} > "$REPORT_FILE"

success "Compilation report saved to $REPORT_FILE"

# Final summary
echo ""
if [ $FAILURE_COUNT -eq 0 ]; then
    success "All $SUCCESS_COUNT document(s) compiled successfully!"
    echo ""
    echo "Generated PDF files:"
    for doc in "${DOCUMENTS[@]}"; do
        if [ -f "${doc}.pdf" ]; then
            echo "  • ${doc}.pdf"
        fi
    done
    exit 0
else
    error "$FAILURE_COUNT document(s) failed to compile"
    exit 1
fi