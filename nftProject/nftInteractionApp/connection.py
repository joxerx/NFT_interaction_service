import yaml
from web3 import Web3, HTTPProvider


def get_config():
    with open("config.yml", 'r') as configfile:
        return yaml.load(configfile, Loader=yaml.FullLoader)


class Connection:
    config = get_config()
    # TODO: Refactor me
    w3 = Web3(Web3.HTTPProvider(config['networks'][0]))
    network = w3.eth
    contract_instance = w3.eth.contract(address=config['contract_address'], abi=config['abi'])

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


connection = Connection()
