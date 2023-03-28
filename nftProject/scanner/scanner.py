import logging

from django.db import IntegrityError

from .utilities import RedisClient
from nftProject.settings import config
from time import sleep
from .serializers import EventSerializer


def get_last_checked_block(contract):
    redis = RedisClient()
    last_checked_block = redis.connection.get(contract)
    if last_checked_block is None:
        last_checked_block = 8500000

    return int(last_checked_block)


def set_last_checked_block(contract, last_block):
    redis = RedisClient()
    redis.connection.set(contract, last_block)


def start_polling():
    while True:
        for network in config.networks:
            last_network_block = network.connection_handler.eth.get_block_number()
            logging.info(f'Get last network block: {last_network_block}')

            last_checked_block = get_last_checked_block(network.name)
            logging.info(f'Get last checked block: {last_checked_block}')

            if last_checked_block >= last_network_block - network.confirmation_gap:
                logging.info("No new blocks. Waiting")
                sleep(120)
                continue

            # If at this moment got too wide interval blocks to check
            # need to decrease top border
            if last_network_block - last_checked_block > network.max_filter_length:
                last_network_block = last_checked_block + network.max_filter_length

            for contract in network.contracts:
                for contract_event in contract.events:
                    event_filter = network.connection_handler.eth.filter({
                        "address": contract.address,
                        "topics": [contract_event],
                        "fromBlock": last_checked_block,
                        "toBlock": last_network_block,
                    })
                    events_list = event_filter.get_all_entries()
                    if events_list:
                        for event in events_list:
                            save_event_to_db(network.name, contract_event, event)
                    else:
                        logging.info(f'No needed events from {last_checked_block} to {last_network_block}')
            set_last_checked_block(network.name, last_network_block)


def save_event_to_db(network, event_name, event: dict):
    # name, address, blockHash,blockNumber,transactionHash,removed,
    data = {
        "name": network + '_' + event_name,
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
