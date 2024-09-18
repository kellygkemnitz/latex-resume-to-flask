import os
from pdflatex import PDFLaTeX
import argparse

templates_dir = 'templates/'
resumes_dir = 'resumes/'

# Create the parser
parser = argparse.ArgumentParser(description='A Python script to convert a resume template in LaTeX format to a PDF, based on type of role.')

parser.add_argument(
    '-t', '--type',
    type=str,
    choices=['it_analyst', 'qa_engineer', 'qa_analyst', 'software_engineer', 'site_reliability_engineer'],
    required=True,
    help='Type of resume to generate')

args = parser.parse_args()

try:
    pdfl = PDFLaTeX.from_texfile(os.path.join(templates_dir, f'{args.type}.tex'))
    pdfl.set_output_directory(resumes_dir)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    print(f'{args.type} PDF generated successfully and placed in {resumes_dir}')
except Exception as e:
    print(f'An error occurred: {e}')