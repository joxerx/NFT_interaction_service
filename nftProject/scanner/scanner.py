import logging

from django.db import IntegrityError
from nftInteractionApp.connection import connection

from .utilities import RedisClient
from nftProject.settings import config
from time import sleep
from .serializers import EventSerializer


class EventHandler:
    network: connection.w3
    contract_address: str

    def __init__(self, network, contract_address):
        self.network = network
        self.contract_address = contract_address


def get_last_checked_block(contract):
    redis = RedisClient()
    last_checked_block = redis.connection.get(contract)
    if last_checked_block is None:
        last_checked_block = 8200000

    return int(last_checked_block)


def set_last_checked_block(contract, last_block):
    redis = RedisClient()
    redis.connection.set(contract, last_block)


class Scanner:
    def __init__(
            self,
            event_handler: EventHandler,
            event_name: str,
    ):
        self.event_handler = event_handler
        self.event_name = event_name

    def start_polling(self):
        while True:
            last_network_block = self.event_handler.network.eth.get_block_number()
            logging.info(f'Get last network block: {last_network_block}')

            last_checked_block = get_last_checked_block(self.event_handler.contract_address)
            logging.info(f'Get last checked block: {last_checked_block}')

            if last_checked_block >= last_network_block - 8:
                logging.info("No new blocks. Waiting")
                sleep(120)
                continue

            # If at this moment got too wide interval blocks to check
            # need to decrease top border
            if last_network_block - last_checked_block > 1000:
                last_network_block = last_checked_block + 990

            event_filter = self.event_handler.network.eth.filter({
                "address": config.contract_address,
                "topics": [config.event_name],
                "fromBlock": last_checked_block,
                "toBlock": last_network_block,
            })
            events_list = event_filter.get_all_entries()
            if events_list:
                for event in events_list:
                    self.save_event_to_db(event)
            else:
                logging.info(f'No needed events from {last_checked_block} to {last_network_block}')
            set_last_checked_block(self.event_handler.contract_address, last_network_block)

    def save_event_to_db(self, event: dict):
        # name, address, blockHash,blockNumber,transactionHash,removed,
        data = {
            "name": self.event_name,
            "address": str(event.address),
            "blockHash": str(event.blockHash.hex()),
            "blockNumber": int(event.blockNumber),
            "transactionHash": str(event.transactionHash.hex()),
            "removed": str(event.removed),
            "logIndex": int(event.logIndex),
        }
        serializer = EventSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.info(f'New event: {data}')
        except IntegrityError:
            logging.info(f'Event with txn hash: {event.transactionHash.hex()} already exists!')
