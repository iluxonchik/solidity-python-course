# as long as SimpleStorage is compilied, we can import it here directly like a Python class
from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # use one of the accounts automatically generated by brownie
    account = get_account()

    # brownie knows wether we need to "transact" or "call"
    # IMPORTANT: every time we do a transaction/"transact" in brownie, we need to add a "from"
    #  The mandatory "from" makes sense, because when reading off of the blockchain, we don't even
    #  need an account, we can just go and look up the data on the blockchain since it's public, but
    #  new transactions on the blockchain change its state, and that requires funds, and we need to
    #  specify from which account that change on the blockchai nwill be introduced.
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(f"{stored_value=}")

    # we are doing a transaction, so we need the "from"
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)  # wait for 1 blocks
    updated_stored_value = simple_storage.retrieve()
    print(f"{updated_stored_value=}")


def get_account():
    # use one of the accounts automatically generated by brownie
    # account = accounts[0]

    # load an account from name, added with "brownie account add"
    # account = accounts.load("account_name")

    # load account directly from a private key
    # account = accounts.add(config["wallets"]["from_key"]) # read from brownie-config.yaml

    if network.show_active() == "development":
        # use one of the accounts automatically generated by brownie
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
