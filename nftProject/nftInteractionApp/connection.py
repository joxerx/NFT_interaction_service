import logging
from typing import List

import yaml
from web3 import Web3, HTTPProvider

from nftProject.settings import config, Network, Contract


class Connection:
    networks: List[Network]
    # FIXME: Now crushing during ABI initializing
    def __init__(self, config):
        self.networks = config.networks
        for network in config.networks:
            if network.type == 'ETHEREUM_LIKE':
                logging.info(f'{network.name} is connected now!')
                print(network.contracts)
                for contract in network.contracts:
                    print(network.instance(contract.name))

    # contract_instance = w3.eth.contract(address=config['contract_address'], abi=config['abi'])
    def send_transaction(self, owner, unique_hash, media_url):
        private_key = self.config['sender_private_key']
        nonce = self.w3.eth.get_transaction_count(f'{self.config["sender_address"]}')
        contract_txn = self.contract_instance.functions.mint(
            owner,
            unique_hash,
            media_url
        ).build_transaction({
            'nonce': nonce,
        })

        signed_txn = self.w3.eth.account.sign_transaction(contract_txn, private_key)
        return self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)


connection = Connection(config)
