#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from scanner.scanner import Scanner, EventHandler
from nftProject.settings import config
from nftInteractionApp.connection import connection

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nftProject.settings')
    # FIXME: Add threading
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

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
