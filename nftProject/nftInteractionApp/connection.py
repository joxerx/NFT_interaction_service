import yaml
from web3 import Web3, HTTPProvider


def get_config():
    with open("config.yml", 'r') as configfile:
        return yaml.load(configfile, Loader=yaml.FullLoader)


class Connection:
    config = get_config()
    w3 = Web3(Web3.HTTPProvider(f'https://goerli.infura.io/v3/{config["infura_key"]}'))
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
