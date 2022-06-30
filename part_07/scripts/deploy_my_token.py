from scripts.utils import get_account
from brownie import ILYToken

from web3 import Web3


def deploy_my_token():
    account = get_account()
    ily_token = ILYToken.deploy(Web3.toWei(6900, "ether"), {"from": account})
    print("contract deployed!")
    return ily_token


def main():
    deploy_my_token()
