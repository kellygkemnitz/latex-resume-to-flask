import logging
import shutil

from modules.config import Config

from pathlib import Path
from pdflatex import PDFLaTeX
from pdf2docx import Converter
from typing import Optional, List

config = Config()
logger = logging.getLogger(__name__)



class PyLaTeXConverter:
    def __init__(self, name: List[str], role_type: str) -> None:
        self.full_name = ' '.join(name).strip()
        self.role_type = role_type

        if self.role_type not in config.ROLE_MAPPING:
            raise ValueError(f"Invalid role type: {self.role_type}. Must be one of {list(config.ROLE_MAPPING.keys())}.")
        
        self.pdf_filename = f'{self.full_name} - {config.ROLE_MAPPING[self.role_type]}'

    def latex_to_pdf(self) -> Optional[Path]:
        try:
            # Use pflatex to make conversion from .tex to .pdf
            config.RESUMES_DIR.mkdir(parents=True, exist_ok=True)
            config.STATIC_DIR.mkdir(parents=True, exist_ok=True)

            template_file = config.TEMPLATES_DIR / f'{self.role_type}.tex'
            if not template_file.exists():
                raise FileNotFoundError(f'Template file {template_file} does not exist.')

            pdf = PDFLaTeX.from_texfile(config.TEMPLATES_DIR / f'{self.role_type}.tex')
            
            pdf_bytes, log, completed_process = pdf.create_pdf(
                keep_pdf_file=False, keep_log_file=False
            )
            
            # Create .pdf filename in resumes/ dir using filename {full_name} - {human-readable role}
            generated_pdf = config.RESUMES_DIR / f'{self.pdf_filename}.pdf'
            with open(generated_pdf, 'wb') as f:
                f.write(pdf_bytes)
            
            logger.info(f'Successfully created {generated_pdf}')

            return generated_pdf

        except Exception as e:
            logger.error(f'An error occurred: {e}')
    
    def pdf_to_docx(self, pdf: Path) -> Optional[Path]:
        try:
            cv = Converter(pdf)

            docx_filename = f'{self.full_name} - {config.ROLE_MAPPING[self.role_type]}.docx'
            generated_docx = config.RESUMES_DIR / docx_filename
            cv.convert(generated_docx, start=0, end=None)

            cv.close()

            logger.info(f'Successfully created {generated_docx}')
        
        except Exception as e:
            logger.error(f'An error occurred: {e}')

    def save_to_static(self, file: Path) -> None:
        try:
            shutil.copy(file, config.STATIC_DIR / 'resume.pdf')
            logger.info(f'Copied {file} to static directory.')
        except Exception as e:
            logger.error(f'An error occurred while copying to static directory: {e}')