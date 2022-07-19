from lib2to3.pgen2.literals import simple_escapes
from scripts.utils import get_account, OPENSEA_TESTNET_FORMAT
from brownie import SimpleCollectible

SIMPLE_TOKEN_URI: str = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(SIMPLE_TOKEN_URI, {"from": account})
    tx.wait(1)
    print(
        f"Your NFT is now available at: {OPENSEA_TESTNET_FORMAT.format(simple_collectible.address, simple_collectible.tokenCounter() - 1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()
