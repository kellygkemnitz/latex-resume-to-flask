import argparse
import os
from pathlib import Path
from pdflatex import PDFLaTeX


templates_dir = Path('templates/')
resumes_dir = Path('resumes/')
static_dir = Path('static/')

def latex_to_pdf():
    """
    A Python script to convert a resume template in LaTeX format to a PDF, based on the type of role.

    This script performs the following steps:
    1. Parses command-line arguments to determine the type of resume and the name to use in the filename.
    2. Maps the role type to a human-readable format.
    3. Uses the pdflatex library to generate a PDF from a LaTeX template.
    4. Copies the generated PDF to a static directory with a generic filename.

    Command-line arguments:
    -t, --type: Type of resume to generate. Choices are ['it_analyst', 'qa_engineer', 'qa_analyst', 'sdet', 'software_dev', 'sre']. Default is 'qa_engineer'.
    -n, --name: Name to use in the filename. This argument is required and can consist of multiple words.

    Example usage:
    python script.py -t qa_engineer -n "John Doe"

    Raises:
    Exception: If an error occurs during the PDF generation or file copying process.
    """

    # Create the parser
    parser = argparse.ArgumentParser(description='A Python script to convert a resume template in LaTeX format to a PDF, based on type of role.')

    parser.add_argument(
        '-t', '--type',
        type=str,
        choices=['it_analyst', 'qa_engineer', 'qa_analyst', 'sdet', 'software_dev', 'sre'],
        default='qa_engineer',
        help='Type of resume to generate'
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        nargs='+',
        required=True,
        help='Name to use in filename'
    )

    args = parser.parse_args()
    full_name = ' ' .join(args.name)

    # Map role type to human-redable format
    type_mapping = {
        'it_analyst': 'IT Analyst',
        'qa_engineer': 'Quality Assurance Engineer',
        'qa_analyst': 'Quality Assurance Analyst',
        'sdet': 'Software Development Engineer in Test',
        'software_dev': 'Software Developer',
        'sre': 'Site Reliability Engineer'
    }

    try:
        # Use pflatex to make conversion from .tex to .pdf
        pdfl = PDFLaTeX.from_texfile(templates_dir / f'{args.type}.tex')
        pdfl.set_output_directory(resumes_dir)
        pdf_filename = f'{full_name} - {type_mapping[args.type]}'
        pdfl.set_pdf_filename(pdf_filename)
        pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
        
        # Create .pdf filename in resumes/ dir using filename {full_name} - {human-readable role}
        generated_pdf = resumes_dir / f'{pdf_filename}.pdf'
        print(f'Successfully created {generated_pdf}')

        # Also create resume.pdf in static/ directory to be used by Flask
        generic_pdf = static_dir / 'resume.pdf'
        os.system(f'cp "{generated_pdf}" "{generic_pdf}"')
        print(f'Succesfully created {generic_pdf}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == "__main__":
    latex_to_pdf()
