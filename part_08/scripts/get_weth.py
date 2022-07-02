from scripts.utils import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    """
    Obtain WETH by depositing ETH into a specific contract.
    """
    # As always, to ineract with a contract, we're going to need:
    #   1. ABI
    #   2. Address
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10**18})
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
