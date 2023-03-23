from django.core.management.base import BaseCommand
from scanner.scanner import Scanner, EventHandler
from nftProject.settings import config
from nftInteractionApp.connection import connection


class Command(BaseCommand):
    help = "Start event scanner"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Scanner is starting..."))

        network_connection = connection.w3
        event_handler = EventHandler(
            network=network_connection,
            contract_address=config.contract_address
        )
        scanner = Scanner(
            event_handler=event_handler,
            event_name=config.event_name
        )
        scanner.start_polling()
