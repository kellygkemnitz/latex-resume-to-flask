from modules.pylatex_converter import PyLaTeXConverter
import argparse

parser = argparse.ArgumentParser(
        description='A Python script to convert a resume template in LaTeX format to .pdf and .docx formats, based on type of role.'
    )

parser.add_argument(
    '-r', '--role',
    type=str,
    choices=['default', 'default_alt', 'it_analyst', 'qa_engineer', 'qa_analyst', 'sdet', 'sw_dev', 'sw_eng', 'sre'],
    default='default_alt',
    help='Role for resume template (default: default_alt)'
)

parser.add_argument(
    '-n', '--name',
    type=str,
    nargs='+',
    required=True,
    help='Name for the resume (e.g., John Doe)'
)

parser.add_argument(
    '-f', '--format',
    type=str,
    required=False,
    choices=['pdf', 'docx', 'both'],
    default='pdf',
    help='Output format: pdf, docx, or both'
)

args = parser.parse_args()

try:
    resume_generator = PyLaTeXConverter(args.name, args.role)
    generated_pdf = resume_generator.latex_to_pdf()

    if generated_pdf:
        resume_generator.save_to_static(generated_pdf)

    if generated_pdf and args.format in ['docx', 'both']:
        generated_docx = resume_generator.pdf_to_docx(generated_pdf)

except Exception as e:
    print(f'An error occurred: {e}')