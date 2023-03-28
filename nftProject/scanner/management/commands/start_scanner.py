from django.core.management.base import BaseCommand
from scanner.scanner import start_polling


class Command(BaseCommand):
    help = "Start event scanner"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Scanner is starting..."))

        start_polling()
