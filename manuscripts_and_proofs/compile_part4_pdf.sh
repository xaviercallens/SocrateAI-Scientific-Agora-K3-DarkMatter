#!/bin/bash

# Script to compile Part IV LaTeX document to PDF
# This script can be run in a Docker container with LaTeX installed

echo "📄 Compiling Part IV LaTeX document to PDF..."

# Check if we're in the right directory
if [ ! -f "Part_IV_Complete_With_Lean_Proofs.tex" ]; then
    echo "❌ Error: Part_IV_Complete_With_Lean_Proofs.tex not found"
    echo "Please run this script from manuscripts_and_proofs/ directory"
    exit 1
fi

# Check for LaTeX compilers
if command -v pdflatex &> /dev/null; then
    COMPILER="pdflatex"
elif command -v xelatex &> /dev/null; then
    COMPILER="xelatex"
elif command -v lualatex &> /dev/null; then
    COMPILER="lualatex"
else
    echo "❌ No LaTeX compiler found (pdflatex, xelatex, or lualatex)"
    echo ""
    echo "Installation options:"
    echo "1. Install TeX Live: sudo apt-get install texlive texlive-latex-extra"
    echo "2. Use Docker: docker run -it --rm -v \$(pwd):/workdir texlive/texlive:latest"
    echo "3. Use Overleaf: Upload to https://www.overleaf.com/"
    exit 1
fi

echo "✅ Found LaTeX compiler: $COMPILER"

# Compile the document
echo "🔄 Compiling Part_IV_Complete_With_Lean_Proofs.tex..."

# First pass
$COMPILER -interaction=nonstopmode Part_IV_Complete_With_Lean_Proofs.tex || {
    echo "⚠️  First compilation pass had warnings/errors, trying again..."
    sleep 2
}

# Second pass (for references)
$COMPILER -interaction=nonstopmode Part_IV_Complete_With_Lean_Proofs.tex || {
    echo "⚠️  Second compilation pass had warnings/errors..."
    sleep 2
}

# Third pass (final)
$COMPILER -interaction=nonstopmode Part_IV_Complete_With_Lean_Proofs.tex || {
    echo "❌ Compilation failed after multiple attempts"
    exit 1
}

# Check if PDF was created
if [ -f "Part_IV_Complete_With_Lean_Proofs.pdf" ]; then
    echo "✅ PDF successfully created: Part_IV_Complete_With_Lean_Proofs.pdf"
    echo ""
    echo "File size: $(du -h Part_IV_Complete_With_Lean_Proofs.pdf | cut -f1)"
    echo "Page count: $(pdfinfo Part_IV_Complete_With_Lean_Proofs.pdf 2>/dev/null | grep Pages | awk '{print $2}' || echo "unknown")"
    echo ""
    echo "📄 PDF compilation successful!"
else
    echo "❌ PDF file was not created"
    exit 1
fi

# Clean up auxiliary files
echo "🧹 Cleaning up auxiliary files..."
rm -f Part_IV_Complete_With_Lean_Proofs.aux Part_IV_Complete_With_Lean_Proofs.log Part_IV_Complete_With_Lean_Proofs.out Part_IV_Complete_With_Lean_Proofs.toc Part_IV_Complete_With_Lean_Proofs.bbl Part_IV_Complete_With_Lean_Proofs.blg

echo "✅ Compilation complete!"
echo "📁 Output: Part_IV_Complete_With_Lean_Proofs.pdf"
