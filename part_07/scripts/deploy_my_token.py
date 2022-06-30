from scripts.utils import get_account
from brownie import ILYToken


def deploy_my_token():
    account = get_account()
    ily_token = ILYToken.deploy(69, {"from": account})
    print("contract deployed!")
    return ily_token


def main():
    deploy_my_token()
