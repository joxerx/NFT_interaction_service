import logging
from typing import List

import yaml
from web3 import Web3, HTTPProvider

from nftProject.settings import config, Network, Contract


class Connection:
    networks: List[Network]

    def __init__(self, config):
        self.networks = config.networks
        for network in config.networks:
            if network.type == 'ETHEREUM_LIKE':
                logging.info(f'{network.name} is connected now!')

    def get_network_object_by_name(self, network_name):
        for network in self.networks:
            if network.name == network_name:
                return network

    def send_transaction(self, network_name, contract_name, owner, unique_hash, media_url):
        network = self.get_network_object_by_name(network_name)
        private_key = network.sender_private_key
        nonce = network.connection_handler.eth.get_transaction_count(network.sender_address)
        contract_instance = network.instance(contract_name)

        contract_txn = contract_instance.functions.mint(
            owner,
            unique_hash,
            media_url
        ).build_transaction({
            'nonce': nonce,
        })
        signed_txn = network.connection_handler.eth.account.sign_transaction(contract_txn, private_key)
        return network.connection_handler.eth.send_raw_transaction(signed_txn.rawTransaction)


connection = Connection(config)
