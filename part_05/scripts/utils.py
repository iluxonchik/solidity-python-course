from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    active_network: str = network.show_active()
    if (
        active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        # use one of the accounts automatically generated by brownie
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # if we are on a development network, we are going to deploy a mock of the ETH/USD data feed.
    # we store the Mock contracts manually in contracts/test, and we copied them from a GitHub repo
    # https://github.com/smartcontractkit/chainlink-mix
    # That repository contains an umplimented version of the original contract, but with the same interface,
    # thus it being a "mock"
    print("Deploying Mocks...")
    # only deploy the mock if it has not yet been deployed
    verify: bool
    try:
        verify = config["networks"][network.show_active()]["verify"]
    except KeyError:
        verify = False
    if len(MockV3Aggregator) <= 0:
        mock_v3_aggr = MockV3Aggregator.deploy(
            8,
            200000000000,
            {"from": get_account()},
            publish_source=verify,
        )
