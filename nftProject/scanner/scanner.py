import logging
from nftInteractionApp.connection import connection
from .utilities import RedisClient
from nftProject.settings import config
from time import sleep
from .serializers import EventSerializer


# FIXME: Fix logging
# TODO: Rewrite
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
        last_checked_block = 8500000

    return int(last_checked_block)


def set_last_checked_block(contract, last_block):
    redis = RedisClient()
    print(f'Setting last checked block: {last_block}')
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
            print(f'Get last network block: {last_network_block}')

            last_checked_block = get_last_checked_block(self.event_handler.contract_address)
            logging.info(f'Get last checked block: {last_checked_block}')
            print(f'Get last checked block: {last_checked_block}')
            if last_checked_block >= last_network_block - 8:
                print("No new blocks. Waiting")
                sleep(220)
                continue
            if last_network_block - last_checked_block > 9000:
                last_network_block = last_checked_block + 8990

            event_filter = self.event_handler.network.eth.filter({
                "address": config.contract_address,
                "topics": [config.event_name],
                "fromBlock": last_checked_block,
                "toBlock": last_network_block,
            })
            events_list = event_filter.get_all_entries()
            if events_list:
                for event in events_list:
                    logging.info(f'New event:{str(event)}')
                    #print(f'New event:{event}')
                    self.save_event_to_db(event)

                file = open(f'events_{last_checked_block}.txt', 'w')
                file.write(str(events_list))
            else:
                logging.info(f'No needed events from {last_checked_block} to {last_network_block}')
            set_last_checked_block(self.event_handler.contract_address, last_network_block)

    def save_event_to_db(self, event: dict):
        # name, address, blockHash,blockNumber,transactionHash,removed,
        data = {
            "name": self.event_name,
            "address": str(event.address),
            "blockHash": str(event.blockHash.hex()),
            "blockNumber": str(event.blockNumber),
            "transactionHash": str(event.transactionHash.hex()),
            "removed": str(event.removed)
        }

        print(data)
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save()