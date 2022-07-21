from scripts.utils import get_account, fund_contract_with_link
from brownie import AdvancedCollectible
from web3 import Web3


def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_contract_with_link(
        advanced_collectible.address, amount=Web3.toWei(0.1, "ether")
    )
    create_collectible_tx = advanced_collectible.createCollectible({"from": account})
    create_collectible_tx.wait(1)
    print("Collectible created!")


def main():
    create_collectible()
