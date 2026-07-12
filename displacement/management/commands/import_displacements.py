import os

from django.core.management.base import BaseCommand

from displacement.services.import_service import import_displacements_from_excel


class Command(BaseCommand):
    help = "Imports displacements from a local Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the Excel file")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        if not os.path.exists(file_path):
            self.stderr.write(f"File not found: {file_path}")
            return

        self.stdout.write("Starting import...")
        try:
            created_count, _ = import_displacements_from_excel(file_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Import completed successfully. Created: {created_count}"
                )
            )
        except Exception as e:
            self.stderr.write(f"Error occurred: {str(e)}")
