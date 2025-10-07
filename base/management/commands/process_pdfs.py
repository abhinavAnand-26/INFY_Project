# base/management/commands/process_pdfs.py
# CREATE THIS FILE in: base/management/commands/process_pdfs.py
# You'll need to create the folders: base/management/commands/

from django.core.management.base import BaseCommand
from base.models import PDFDocument
from base.pdf_processor import process_pdf_document

class Command(BaseCommand):
    help = 'Process uploaded PDF documents to extract questions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Process all unprocessed PDFs',
        )
        parser.add_argument(
            '--id',
            type=int,
            help='Process specific PDF by ID',
        )

    def handle(self, *args, **options):
        if options['id']:
            # Process specific PDF
            success, message = process_pdf_document(options['id'])
            if success:
                self.stdout.write(self.style.SUCCESS(message))
            else:
                self.stdout.write(self.style.ERROR(message))
        
        elif options['all']:
            # Process all unprocessed PDFs
            unprocessed_pdfs = PDFDocument.objects.filter(is_processed=False)
            
            if not unprocessed_pdfs.exists():
                self.stdout.write(self.style.WARNING('No unprocessed PDFs found'))
                return
            
            total = unprocessed_pdfs.count()
            processed = 0
            failed = 0
            
            for pdf_doc in unprocessed_pdfs:
                self.stdout.write(f"Processing: {pdf_doc.title}...")
                success, message = process_pdf_document(pdf_doc.id)
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f"✓ {message}"))
                    processed += 1
                else:
                    self.stdout.write(self.style.ERROR(f"✗ {message}"))
                    failed += 1
            
            self.stdout.write(self.style.SUCCESS(f"\nTotal: {total} | Processed: {processed} | Failed: {failed}"))
        
        else:
            self.stdout.write(self.style.WARNING('Please specify --all or --id <pdf_id>'))