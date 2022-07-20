from lib2to3.pgen2.literals import simple_escapes
from scripts.utils import (
    get_account,
    OPENSEA_TESTNET_FORMAT,
    get_contract,
    fund_contract_with_link,
)
from brownie import AdvancedCollectible, config, network

SIMPLE_TOKEN_URI: str = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
    )
    fund_contract_with_link(advanced_collectible.address)
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    print("Token has been created")


def main():
    deploy_and_create()
