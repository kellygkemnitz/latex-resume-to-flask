<<<<<<< HEAD
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
=======
from modules.latex_converter import ResumeGenerator
import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Generate resume files in PDF and DOCX formats from LaTeX templates'
    )

    parser.add_argument(
        '-t', '--type',
        type=str,
        choices=list(ResumeGenerator.TYPE_MAPPING.keys()),
        default='qa_engineer',
        help='Type of resume template to use'
    )

    parser.add_argument(
        '-n', '--name',
        type=str,
        nargs='+',
        help='Full name for the resume (can be multiple words)'
    )
    
    parser.add_argument(
        '-f', '--formats',
        type=str,
        nargs='+',
        choices=['pdf', 'docx'],
        default=['pdf'],
        help='Output formats to generate (default: pdf only)'
    )
    
    parser.add_argument(
        '--list-templates',
        action='store_true',
        help='List available resume templates and exit'
    )

    args = parser.parse_args()
    
    # Handle template listing
    if args.list_templates:
        templates = ResumeGenerator.get_available_templates()
        print("Available templates:")
        for template in sorted(templates):
            description = ResumeGenerator.TYPE_MAPPING.get(template, template)
            print(f"  {template:<15} - {description}")
        return 0

    # Validate required arguments for resume generation
    if not args.name:
        print("Error: Name is required for resume generation", file=sys.stderr)
        parser.print_help()
        return 1

    try:
        resume_generator = ResumeGenerator(args.name, args.type)
        results = resume_generator.generate_resume(args.formats)
        
        print("\nGenerated files:")
        for format_type, file_path in results.items():
            print(f"  {format_type.upper()}: {file_path}")
        
        return 0
        
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
>>>>>>> 2180e871bf89c3a74aa8badc6a6041423c222c5d
