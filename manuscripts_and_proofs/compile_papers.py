#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import shutil

# List of target tex files to compile
TARGET_PAPERS = [
    "PaperV_Global_Topological_Theory.tex",
    "Paper_IVB_StringPhenomenology.tex",
    "Part_III_Feynman_K3_Mapping.tex",
    "Part_II_Vafa_DarkEnergy.tex",
    "Part_IVC_ComputationalMath.tex",
    "Part_IV_A_Resolving the Fuzzy Dark Matter Tension via Environment-Dependent Scalar Fields - PTA Signatures and Bayesian Inference Framework.tex",
    "Part_IV_Complete_With_Lean_Proofs.tex",
    "Part_IV_Rigorous_Resolution_FDM_Tension.tex"
]

WORKDIR = os.path.dirname(os.path.abspath(__file__))

def get_page_count(pdf_path):
    try:
        # Attempt to use pdfinfo
        res = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            if line.startswith("Pages:"):
                return line.split()[1]
    except Exception:
        pass
    return "N/A"

def get_file_size(filepath):
    try:
        size_bytes = os.path.getsize(filepath)
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    except Exception:
        return "N/A"

def clean_aux_files(base_name):
    # We clean up helper compilation files but keep log/pdf/synctex
    extensions = [".aux", ".out", ".toc", ".blg", ".nav", ".snm", ".synctex.gz"]
    for ext in extensions:
        path = os.path.join(WORKDIR, base_name + ext)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

def compile_paper(tex_filename):
    base_name = os.path.splitext(tex_filename)[0]
    tex_path = os.path.join(WORKDIR, tex_filename)
    pdf_path = os.path.join(WORKDIR, base_name + ".pdf")
    
    # Remove existing PDF first so we know if compilation fails to produce a new one
    if os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    print(f"\n==================================================")
    print(f"📖 Compiling: {tex_filename}")
    print(f"==================================================")

    # Pass 1
    print("🚀 [Pass 1] Running pdflatex...")
    cmd1 = ["pdflatex", "-interaction=nonstopmode", tex_filename]
    res1 = subprocess.run(cmd1, cwd=WORKDIR, capture_output=True, text=True, errors="replace")
    
    # Check if we should run BibTeX
    # BibTeX is run if there are citations or if .aux indicates bibliography
    aux_path = os.path.join(WORKDIR, base_name + ".aux")
    has_bib = False
    if os.path.exists(aux_path):
        with open(aux_path, "r", encoding="utf-8", errors="ignore") as f:
            aux_content = f.read()
            if "\\bibdata" in aux_content or "\\citation" in aux_content:
                has_bib = True

    if has_bib:
        print("📚 Running BibTeX...")
        cmd_bib = ["bibtex", base_name]
        res_bib = subprocess.run(cmd_bib, cwd=WORKDIR, capture_output=True, text=True, errors="replace")
        if res_bib.returncode != 0:
            print(f"⚠️ BibTeX warning/error (continuing): {res_bib.stderr.strip()}")
    
    # Pass 2
    print("🚀 [Pass 2] Running pdflatex...")
    res2 = subprocess.run(cmd1, cwd=WORKDIR, capture_output=True, text=True, errors="replace")
    
    # Pass 3
    print("🚀 [Pass 3] Running pdflatex...")
    res3 = subprocess.run(cmd1, cwd=WORKDIR, capture_output=True, text=True, errors="replace")

    # Check result
    if os.path.exists(pdf_path):
        size = get_file_size(pdf_path)
        pages = get_page_count(pdf_path)
        print(f"✅ Success! Generated {base_name}.pdf ({size}, {pages} pages)")
        clean_aux_files(base_name)
        return {
            "status": "Success",
            "size": size,
            "pages": pages,
            "error": None
        }
    else:
        # Try to extract the LaTeX error from log
        log_path = os.path.join(WORKDIR, base_name + ".log")
        error_msg = "Unknown pdflatex compilation error."
        if os.path.exists(log_path):
            errors = []
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith("!"):
                        err_context = "".join(lines[max(0, i-1):min(len(lines), i+4)])
                        errors.append(err_context)
            if errors:
                error_msg = "\n---\n".join(errors[:3])
            else:
                # Fallback to last 20 lines of log
                error_msg = "".join(lines[-20:])
                
        print(f"❌ Failed to compile {tex_filename}!")
        print(f"Error Details:\n{error_msg}")
        return {
            "status": "Failed",
            "size": "N/A",
            "pages": "N/A",
            "error": error_msg
        }

def main():
    print(f"Starting compilation of {len(TARGET_PAPERS)} LaTeX files in:")
    print(f"📁 {WORKDIR}\n")
    
    results = {}
    for paper in TARGET_PAPERS:
        if not os.path.exists(os.path.join(WORKDIR, paper)):
            print(f"⚠️ File not found: {paper}")
            results[paper] = {
                "status": "Missing File",
                "size": "N/A",
                "pages": "N/A",
                "error": "The specified .tex file does not exist in the repository manuscripts folder."
            }
            continue
            
        results[paper] = compile_paper(paper)
        
    print("\n\n==================================================")
    print("📊 COMPILATION SUMMARY REPORT")
    print("==================================================")
    
    success_count = sum(1 for r in results.values() if r["status"] == "Success")
    failed_count = sum(1 for r in results.values() if r["status"] == "Failed")
    missing_count = sum(1 for r in results.values() if r["status"] == "Missing File")
    
    print(f"Total Papers: {len(TARGET_PAPERS)}")
    print(f"🟢 Success:    {success_count}")
    print(f"🔴 Failed:     {failed_count}")
    if missing_count > 0:
        print(f"🟡 Missing:    {missing_count}")
        
    # Write a Markdown report file
    report_path = os.path.join(WORKDIR, "compilation_summary.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🔬 Agora Manuscript PDF Compilation Report\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Working Directory:** `{WORKDIR}`\n\n")
        f.write("## 📊 Summary Metrics\n\n")
        f.write(f"- **Total Target Manuscripts:** {len(TARGET_PAPERS)}\n")
        f.write(f"- **Successfully Compiled (PDF created):** {success_count} / {len(TARGET_PAPERS)}\n")
        f.write(f"- **Failed Compilation:** {failed_count}\n")
        if missing_count > 0:
            f.write(f"- **Missing Source Files:** {missing_count}\n")
        f.write("\n---\n\n")
        
        f.write("## 📄 Detailed Status Table\n\n")
        f.write("| Manuscript / .tex File | Status | Pages | File Size | PDF Link |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        
        for paper in TARGET_PAPERS:
            p_res = results[paper]
            base_name = os.path.splitext(paper)[0]
            status_emoji = "✅" if p_res["status"] == "Success" else "❌" if p_res["status"] == "Failed" else "⚠️"
            pdf_link = f"[Download PDF](./{base_name}.pdf)" if p_res["status"] == "Success" else "N/A"
            f.write(f"| `{paper}` | {status_emoji} **{p_res['status']}** | {p_res['pages']} | {p_res['size']} | {pdf_link} |\n")
            
        f.write("\n---\n\n")
        
        if failed_count > 0:
            f.write("## 🔍 Compilation Failure Details\n\n")
            for paper, p_res in results.items():
                if p_res["status"] == "Failed":
                    f.write(f"### ❌ `{paper}`\n\n")
                    f.write(f"```text\n{p_res['error']}\n```\n\n")
                    
    print(f"\nReport written to: {report_path}")
    if failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
