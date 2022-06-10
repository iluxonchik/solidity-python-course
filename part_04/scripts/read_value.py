"""
Read directly from the Goerli chain
"""
from brownie import SimpleStorage, accounts, config


def read_contract():
    # get the address of the most recent SimpleStorage deployment
    simple_storage = SimpleStorage[-1]

    # in order to read directly from the blockchain we need:
    #  1. address of the contract
    #  2. ABI
    #  The brownie compiled contract abstraction (SimpleStorage) already contains all of that
    #    so all we have to do is just call .retrieve()
    print(simple_storage.retrieve())


def main():
    read_contract()
