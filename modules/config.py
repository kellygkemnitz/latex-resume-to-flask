from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR = BASE_DIR / 'templates'
    RESUMES_DIR = BASE_DIR / 'resumes'
    STATIC_DIR = BASE_DIR / 'app' / 'static'
    ROLE_MAPPING = {
        'default': 'Default',
        'default_alt': 'Default Alt',
        'it_analyst': 'IT Analyst',
        'qa_engineer': 'Quality Assurance Engineer',
        'qa_analyst': 'Quality Assurance Analyst',
        'sdet': 'Software Development Engineer in Test',
        'sw_dev': 'Software Developer',
        'sw_eng': 'Software Engineer',
        'sre': 'Site Reliability Engineer'
    }