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
