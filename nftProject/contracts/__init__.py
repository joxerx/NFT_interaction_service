import json
import os


with open(os.path.dirname(__file__) + "/MintableNFT.json") as f:
    MINTABLE_NFT = json.load(f)
