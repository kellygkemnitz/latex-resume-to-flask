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

type_mapping = {
    'it_analyst': 'IT Analyst',
    'qa_engineer': 'Quality Assurance Engineer',
    'qa_analyst': 'Quality Assurance Analyst',
    'sdet': 'Software Development Engineer in Test',
    'software_dev': 'Software Developer',
    'sre': 'Site Reliability Engineer'
}

try:
    pdfl = PDFLaTeX.from_texfile(os.path.join(templates_dir, f'{args.type}.tex'))
    pdfl.set_output_directory(resumes_dir)
    pdf_filename = f'{full_name} - {type_mapping[args.type]}'
    pdfl.set_pdf_filename(pdf_filename)
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
    print(f'{pdf_filename}.pdf generated successfully and placed in {resumes_dir}')

    os.system(f'cp {pdf_filename}.pdf {os.path.join(resumes_dir), 'resume.pdf'}')

except Exception as e:
    print(f'An error occurred: {e}')