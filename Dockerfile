# Dockerfile for compiling Part IV LaTeX document to PDF
# This provides a complete LaTeX environment with all required packages

FROM texlive/texlive:latest

# Install additional LaTeX packages
RUN tlmgr update --self && \
    tlmgr install \
        collection-fontsrecommended \
        collection-latexextra \
        collection-latexrecommended \
        collection-mathscience \
        collection-pictures \
        collection-plainextra \
        listings \
        fancyvrb \
        hyperref \
        amsmath \
        amssymb \
        amsthm \
        geometry \
        authblk \
        physics \
        tensor \
        xcolor \
        graphicx \
        float \
        url \
        bibtex \
        && \
    tlmgr paper a4 && \
    echo "LaTeX packages installed successfully"

# Set up working directory
WORKDIR /workspace

# Copy the repository contents
COPY . .

# Set up the compilation script
WORKDIR /workspace/manuscripts_and_proofs

# Default command: compile the Part IV document
CMD ["./compile_part4_pdf.sh"]

# Alternative: keep container running for interactive use
# CMD ["/bin/bash"]

# Build and run instructions:
# docker build -t part4-pdf-compiler .
# docker run -it --rm -v $(pwd):/workspace part4-pdf-compiler
# This will create Part_IV_Complete_With_Lean_Proofs.pdf in the manuscripts_and_proofs directory
