from web3 import Web3
from brownie import FundMe, network, config, MockV3Aggregator
from scripts.utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    verify: bool
    price_feed_addr: str
    print(f"Active network: f{network.show_active()}")
    account = get_account()
    try:
        verify = config["networks"][network.show_active()]["verify"]
    except KeyError:
        verify = False
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_mocks()
        price_feed_addr = MockV3Aggregator[-1].address
    else:
        price_feed_addr = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    fund_me = FundMe.deploy(
        price_feed_addr,
        {"from": account},
        publish_source=verify,
    )  # publish source will verify the contract
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
