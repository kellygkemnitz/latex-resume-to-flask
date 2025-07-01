import argparse
import os
import shutil

from pathlib import Path
from pdflatex import PDFLaTeX
from pdf2docx import Converter


class ResumeGenerator:
    def __init__(self, name, resume_type):
        self.templates_dir = Path('templates/')
        self.resumes_dir = Path('resumes/')
        self.static_dir = Path('static/')

        self.full_name = ' '.join(name).strip()
        self.resume_type = resume_type

        self.type_mapping = {
            'it_analyst': 'IT Analyst',
            'qa_engineer': 'Quality Assurance Engineer',
            'qa_analyst': 'Quality Assurance Analyst',
            'sdet': 'Software Development Engineer in Test',
            'software_dev': 'Software Developer',
            'sre': 'Site Reliability Engineer'
        }
        
        if self.resume_type not in self.type_mapping:
            raise ValueError(f"Invalid resume type: {self.resume_type}. Must be one of {list(self.type_mapping.keys())}.")
        
        self.pdf_filename = f'{self.full_name} - {self.type_mapping[self.resume_type]}'

    def latex_to_pdf(self):
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

        try:
            # Use pflatex to make conversion from .tex to .pdf
            self.resumes_dir.mkdir(parents=True, exist_ok=True)
            self.static_dir.mkdir(parents=True, exist_ok=True)

            template_file = self.templates_dir / f'{self.resume_type}.tex'
            if not template_file.exists():
                raise FileNotFoundError(f'Template file {template_file} does not exist.')

            pdf = PDFLaTeX.from_texfile(self.templates_dir / f'{self.resume_type}.tex')
            
            pdf_bytes, log, completed_process = pdf.create_pdf(
                keep_pdf_file=True, keep_log_file=False
            )
            
            # Create .pdf filename in resumes/ dir using filename {full_name} - {human-readable role}
            generated_pdf = self.resumes_dir / f'{self.pdf_filename}.pdf'
            with open(generated_pdf, 'wb') as f:
                f.write(pdf_bytes)
            
            print(f'Successfully created {generated_pdf}')

            # Also create resume.pdf in static/ directory to be used by Flask
            generic_pdf = self.static_dir / 'resume.pdf'
            shutil.copy(generated_pdf, generic_pdf)

            print(f'Succesfully created {generic_pdf}')

            return generated_pdf

        except Exception as e:
            print(f'An error occurred: {e}')
    
    def pdf_to_docx(self, pdf):
        try:
            cv = Converter(pdf)

            docx_filename = f'{self.full_name} - {self.type_mapping[self.resume_type]}.docx'
            generated_docx = f'{self.resumes_dir}/{docx_filename}'
            cv.convert(generated_docx, start=0, end=None)

            cv.close()

            print(f'Succesfully created {generated_docx}')
        
        except Exception as e:
            print(f'An error occurred: {e}')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A Python script to convert a resume template in LaTeX format to .pdf and .docx formats, based on type of role.'
    )

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

    try:
        resume_generator = ResumeGenerator(args.name, args.type)
        generated_pdf = resume_generator.latex_to_pdf()

        if generated_pdf:
            resume_generator.pdf_to_docx(generated_pdf)

    except Exception as e:
        print(f'An error occurred: {e}')