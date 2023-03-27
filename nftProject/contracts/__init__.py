import json
from pathlib import Path


with Path("contracts", "MintableNFT.json").open() as f:
    MINTABLE_NFT = json.load(f)
