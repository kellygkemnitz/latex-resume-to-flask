import logging
import shutil
import tempfile

from pathlib import Path
from pdf2docx import Converter
from pdflatex import PDFLaTeX
from typing import Dict, Optional, Tuple


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeGenerator:
    """A class to generate resumes in PDF and DOCX formats from LaTeX templates."""
    
    # Class constants
    TYPE_MAPPING: Dict[str, str] = {
        'default': 'Default',
        'default_alt': 'Default Alt',
        'it_analyst': 'IT Analyst',
        'qa_engineer': 'Quality Assurance Engineer',
        'qa_analyst': 'Quality Assurance Analyst',
        'sdet': 'Software Development Engineer in Test',
        'sw_dev': 'Software Developer',
        'sw_eng': 'Software Engineer',
        'sre': 'Site Reliability Engineer',
        'faang': 'FAANG'
    }
    
    GENERIC_PDF_NAME = 'resume.pdf'
    
    def __init__(self, name: list[str], resume_type: str, base_dir: Optional[Path] = None) -> None:
        """Initialize the ResumeGenerator.
        
        Args:
            name: List of name components to be joined
            resume_type: Type of resume template to use
            base_dir: Base directory for the project (defaults to current module directory)
        
        Raises:
            ValueError: If resume_type is not supported
            FileNotFoundError: If required directories don't exist
        """
        # Use module directory as base if not provided
        if base_dir is None:
            base_dir = Path(__file__).parent
            
        self.base_dir = base_dir
        self.templates_dir = self.base_dir / 'templates'
        self.resumes_dir = self.base_dir / 'resumes'
        self.static_dir = self.base_dir.parent / 'app' / 'static'

        self.full_name = ' '.join(name).strip()
        self.resume_type = resume_type
        
        self._validate_resume_type()
        self._validate_directories()
        
        self.pdf_filename = f'{self.full_name} - {self.TYPE_MAPPING[self.resume_type]}'
    
    def _validate_resume_type(self) -> None:
        """Validate that the resume type is supported."""
        if self.resume_type not in self.TYPE_MAPPING:
            available_types = ', '.join(self.TYPE_MAPPING.keys())
            raise ValueError(
                f"Invalid resume type: '{self.resume_type}'. "
                f"Must be one of: {available_types}"
            )
    
    def _validate_directories(self) -> None:
        """Validate that required directories exist or can be created."""
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")
        
        # Create output directories if they don't exist
        self.resumes_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(self) -> Path:
        """Generate a PDF resume from LaTeX template.
        
        Returns:
            Path to the generated PDF file
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            RuntimeError: If PDF generation fails
        """
        logger.info(f"Generating PDF for {self.full_name} using {self.resume_type} template")
        
        template_file = self._get_template_file()
        generated_pdf = self._compile_latex_to_pdf(template_file)
        self._copy_to_static_dir(generated_pdf)
        
        logger.info(f"PDF generation completed: {generated_pdf}")
        return generated_pdf
    
    def _get_template_file(self) -> Path:
        """Get and validate the template file path."""
        template_file = self.templates_dir / f'{self.resume_type}.tex'
        if not template_file.exists():
            available_templates = list(self.templates_dir.glob('*.tex'))
            available_names = [t.stem for t in available_templates]
            raise FileNotFoundError(
                f"Template file '{template_file}' does not exist. "
                f"Available templates: {', '.join(available_names)}"
            )
        return template_file
    
    def _compile_latex_to_pdf(self, template_file: Path) -> Path:
        """Compile LaTeX template to PDF."""
        try:
            logger.debug(f"Compiling LaTeX template: {template_file}")
            
            # Check if resume.cls exists in the templates directory
            cls_file = template_file.parent / 'classes' / 'resume.cls'
            has_cls_file = cls_file.exists()
            
            # Create a temporary directory and copy template (and class file if it exists)
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                temp_tex_file = temp_path / template_file.name
                
                # Copy template to temp directory
                shutil.copy2(template_file, temp_tex_file)
                
                # Only copy class file if it exists
                if has_cls_file:
                    temp_cls_file = temp_path / 'resume.cls'
                    shutil.copy2(cls_file, temp_cls_file)
                
                # Create PDFLaTeX object from the temporary template file
                pdf = PDFLaTeX.from_texfile(str(temp_tex_file))
                
                pdf_bytes, log, completed_process = pdf.create_pdf(
                    keep_pdf_file=False, keep_log_file=False
                )
                
                if completed_process.returncode != 0:
                    logger.error(f"LaTeX compilation failed. Log: {log}")
                    raise RuntimeError(f"LaTeX compilation failed with return code {completed_process.returncode}")
            
            # Write PDF to resumes directory
            generated_pdf = self.resumes_dir / f'{self.pdf_filename}.pdf'
            with open(generated_pdf, 'wb') as f:
                f.write(pdf_bytes)
            
            logger.info(f"Successfully created {generated_pdf}")
            return generated_pdf
            
        except Exception as e:
            logger.error(f"Failed to compile LaTeX to PDF: {e}")
            raise RuntimeError(f"PDF generation failed: {e}") from e
    
    def _copy_to_static_dir(self, source_pdf: Path) -> Path:
        """Copy generated PDF to static directory for Flask app."""
        try:
            generic_pdf = self.static_dir / self.GENERIC_PDF_NAME
            shutil.copy2(source_pdf, generic_pdf)
            logger.info(f"Successfully created {generic_pdf}")
            return generic_pdf
        except Exception as e:
            logger.error(f"Failed to copy PDF to static directory: {e}")
            raise
    
    def convert_pdf_to_docx(self, pdf_path: Path) -> Path:
        """Convert PDF resume to DOCX format.
        
        Args:
            pdf_path: Path to the PDF file to convert
            
        Returns:
            Path to the generated DOCX file
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            RuntimeError: If conversion fails
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Converting PDF to DOCX: {pdf_path}")
        
        try:
            docx_filename = f'{self.full_name} - {self.TYPE_MAPPING[self.resume_type]}.docx'
            generated_docx = self.resumes_dir / docx_filename
            
            cv = Converter(str(pdf_path))
            cv.convert(str(generated_docx), start=0, end=None)
            cv.close()
            
            logger.info(f"Successfully created {generated_docx}")
            return generated_docx
            
        except Exception as e:
            logger.error(f"Failed to convert PDF to DOCX: {e}")
            raise RuntimeError(f"DOCX conversion failed: {e}") from e
    
    def generate_resume(self, formats: Optional[list[str]] = None) -> Dict[str, Path]:
        """Generate resume in specified formats.
        
        Args:
            formats: List of formats to generate ['pdf', 'docx']. Defaults to ['pdf']
            
        Returns:
            Dictionary mapping format names to generated file paths
        """
        if formats is None:
            formats = ['pdf']
        
        results = {}
        
        # Always generate PDF first as it's the source for other formats
        if 'pdf' in formats:
            pdf_path = self.generate_pdf()
            results['pdf'] = pdf_path
        
        if 'docx' in formats:
            # Use existing PDF or generate one
            pdf_path = results.get('pdf') or self.generate_pdf()
            docx_path = self.convert_pdf_to_docx(pdf_path)
            results['docx'] = docx_path
        
        return results
    
    @classmethod
    def get_available_templates(cls, base_dir: Optional[Path] = None) -> list[str]:
        """Get list of available resume templates.
        
        Args:
            base_dir: Base directory to search for templates
            
        Returns:
            List of available template names
        """
        if base_dir is None:
            base_dir = Path(__file__).parent
        
        templates_dir = base_dir / 'templates'
        if not templates_dir.exists():
            return []
        
        return [t.stem for t in templates_dir.glob('*.tex') if t.is_file()]
