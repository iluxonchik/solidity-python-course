from scripts.get_weth import get_weth
from scripts.utils import get_account
from brownie import interface, config, network
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() == "mainnet-fork":
        get_weth()
    # When working with a smart contract we need:
    # 1. ABI of the smart contract
    # 2. Address of the smart contract
    lending_pool = get_lending_pool()

    # We need to approve the lending pool to withdraw tokens/money from our ERC20 contract.
    #
    # Internally, that ERC20 contract keeps a track of the balances of all accounts.
    # When we are approving a certain address to move tokens out of another address, the ERC20 contract
    # saves that in its internal state, and then than foreign address is able to transfer out tokens from
    # another address, up to the allowed limit.
    #
    # In our case, the ERC20 token is WETH.
    approve_erc20(
        lending_pool.address,
        AMOUNT,
        erc20_address,
        account,
    )

    # now that we have given the lending pool approval to move ERC20 tokens belonging to our address (WETH),
    # we can deposit
    #
    # IMPORTANT: our address doesn't actually store any tokens in it, the tokens are stored in an ERC20 Contract.
    # That ERC20 contract, has an internal dictionary mapping your address to the amount of tokens that you have.
    # Since ERC20 is a standard, everyone can read out of that address and see how many tokens you have.
    # This is why you need to import a token into Metamask. It simply cannot know which tokens you have, as it would have
    # to scan all of the ERC20 contracts on the blockchain, and see where your address is present as a key in that dictionary.

    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")


def get_lending_pool():
    # When working wtih a contract, we need:
    #   1. ABI, which is the interface used to interact with the contract
    #   2. Address of the smart contract with which we will be interacting via the ABI
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(spender, amount, erc20_address, from_account):
    print("Approving ERC20 token...")
    # When interacting with a contract we need:
    #   1. its ABI
    #   2. its address
    # We will interact with contract located at <addresss> through the <ABI>
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": from_account})
    tx.wait(1)
    print("Approved!")
    return tx
