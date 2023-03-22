from nftInteractionApp.connection import connection
from web3 import Web3
from threading import Thread
import time
import logging

from nftProject.nftInteractionApp.models import Token

# TODO: Change to django logging
logging.basicConfig(
    level=logging.INFO,
    filename="scanner.log",
    format="%(asctime)s %(levelname)s: %(message)s"
)


# TODO: Rewrite
class EventHandler:
    network: Web3.eth
    contract_address: str

    def create(self, network, contract_address):
        self.network = network
        self.contract_address = contract_address


# TODO: write doc
def get_last_block(network):
    return network.block_number


# TODO: fixme
last_checked_block = 8519027


# TODO: convert to async and add sleep
while True:
    last_network_block = get_last_block(w3.eth)
    logging.info(f'Get last network block: {last_network_block}')

    logging.info(f'Get last checked block: {last_checked_block}')

    if last_network_block - last_checked_block > 9000:
        last_network_block = last_checked_block + 8990

    event_filter = network.filter({
        "address": contract_address,
        "topics": [event_name],
        "fromBlock": last_checked_block,
        "toBlock": last_network_block,
    })
    events_list = event_filter.get_all_entries()

    logging.info(f'New events:{events_list}')
    last_checked_block = last_network_block
