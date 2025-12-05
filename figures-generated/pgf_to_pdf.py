import os
import subprocess
import shutil
import tempfile


def convert_pgf_to_pdf(pgf_file_path):
    # Ensure pdflatex is available in the system's PATH
    try:
        subprocess.run(["pdflatex", "--version"], check=True, capture_output=True)
    except FileNotFoundError:
        print("Error: 'pdflatex' command not found.")
        print("Please ensure you have a LaTeX distribution (like TeX Live or MiKTeX)")
        print("installed and 'pdflatex' is added to your system's PATH.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Error checking pdflatex version: {e}")
        print(f"Stderr: {e.stderr.decode()}")
        return

    input_dir = os.path.dirname(pgf_file_path)
    base_filename = os.path.splitext(os.path.basename(pgf_file_path))[0]
    output_pdf_path = os.path.join(input_dir, f"{base_filename}.pdf")

    # Define the LaTeX template
    # The \input command requires the path to be relative to the .tex file
    # or absolute. Using os.path.relpath to ensure it works correctly.
    latex_template = (
        r"""
\documentclass[pgfplots, border=3mm]{standalone}
\usepackage[utf8]{inputenc}
\usepackage{pgfplots}
\usepackage{pgf}
\usepackage{amsmath}
\usepackage{amsfonts} 
\usepackage{amssymb} 
\usepackage{latexsym}
\usepackage{color, colortbl}

\def\mathdefault#1{#1}
  \everymath=\expandafter{\the\everymath\displaystyle}
  \ifdefined\pdftexversion\else  % non-pdftex case.
    \usepackage{fontspec}
  \fi
\makeatletter\@ifpackageloaded{underscore}{}{\usepackage[strings]{underscore}}\makeatother
\usepackage{graphicx}

\usepackage{mathtools}
\usepackage{siunitx}
\sisetup{
    group-separator = {,},
    % uncomment the next line if we also should split numbers of 4 digits, i.e. 1000 -> 1,000, if not then the number needs at least 5 digits to be split, e.g. 10000 -> 10,000 but 9000 -> 9000
    % group-minimum-digits = 4
}

\def\mathdefault#1{#1}
\everymath=\expandafter{\the\everymath\displaystyle}
\newcommand{\pcal}{$\mathcal{P}$ }
\newcommand{\scal}{$\mathcal{S}$ }

\begin{document}

\input{"""
        + os.path.basename(pgf_file_path)
        + r"""}

\end{document}
"""
    )
    # Create a temporary directory for compilation to keep the original folder clean
    # and to handle potential issues with pdflatex outputting to the same dir.
    with tempfile.TemporaryDirectory() as temp_compilation_dir:
        # Copy the .pgf file to the temporary directory
        temp_pgf_path = os.path.join(
            temp_compilation_dir, os.path.basename(pgf_file_path)
        )
        shutil.copy(pgf_file_path, temp_pgf_path)

        # Create the temporary .tex file in the temporary directory
        temp_tex_filename = f"{base_filename}.tex"
        temp_tex_path = os.path.join(temp_compilation_dir, temp_tex_filename)
        with open(temp_tex_path, "w", encoding="utf-8") as f:
            f.write(latex_template)

        print(f"Converting '{pgf_file_path}' to PDF...")

        # We change the current working directory to the temporary directory
        # so pdflatex can find the .pgf file via \input.
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", temp_tex_filename],
                cwd=temp_compilation_dir,
                capture_output=True,
                check=True,  # Raise an exception for non-zero exit codes
                text=True,  # Capture stdout/stderr as text
            )
            generated_pdf_path = os.path.join(
                temp_compilation_dir, f"{base_filename}.pdf"
            )
            if os.path.exists(generated_pdf_path):
                shutil.move(generated_pdf_path, output_pdf_path)
                print(f"Successfully converted and saved as '{output_pdf_path}'")
            else:
                print(
                    f"Error: PDF not generated for '{pgf_file_path}'. Check LaTeX log for details."
                )
                # Optionally print log if PDF wasn't found
                log_path = os.path.join(temp_compilation_dir, f"{base_filename}.log")
                if os.path.exists(log_path):
                    with open(
                        log_path, "r", encoding="utf-8", errors="ignore"
                    ) as log_f:
                        print("--- LaTeX Log (partial) ---")
                        # Print last 20 lines of log for quick debugging
                        log_lines = log_f.readlines()
                        for line in log_lines[-20:]:
                            print(line.strip())
                        print("---------------------------")

        except subprocess.CalledProcessError as e:
            print(f"Error compiling '{pgf_file_path}':")
            print(f"Command: {' '.join(e.cmd)}")
            print(f"Return Code: {e.returncode}")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            print("Please check the .pgf file for LaTeX errors.")
        except Exception as e:
            print(
                f"An unexpected error occurred during conversion of '{pgf_file_path}': {e}"
            )


def main():
    """
    Main function to ask for the root folder and process all .pgf files.
    """
    root_folder = input("Enter the path to the folder containing .pgf files: ").strip()

    if not os.path.isdir(root_folder):
        print(f"Error: The provided path '{root_folder}' is not a valid directory.")
        return

    print(f"\nStarting conversion process in '{root_folder}'...")
    found_pgf_files = False
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(".pgf"):
                found_pgf_files = True
                pgf_file_path = os.path.join(dirpath, filename)
                convert_pgf_to_pdf(pgf_file_path)

    if not found_pgf_files:
        print(f"No .pgf files found in '{root_folder}' or its subfolders.")
    else:
        print("\nConversion process completed.")


if __name__ == "__main__":
    main()
