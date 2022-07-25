from brownie import (
    Box,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)


def main():

    from scripts.utils import get_account, encode_function_data

    account = get_account()

    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": account})

    # not necesasry, but a good practice. we could use our address directly as the admin, instead of
    # relying on a proxy
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # if we want to initialize our proxied contract, we don't use a constrctor. instead, we encode
    # use initializer functions which initialize the proxied contract's internal state. that initiazlier
    # function, alongside its args must be encoded into bytes, and it will be passed into the
    # Solidity's delegatecall() function
    #
    # in our example, we are not using an initializer function, but here is how we could have done it:
    # box_encoded_initializer_function = encode_function_data(initializer=box.store, 1)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,  # the proxied contract
        proxy_admin.address,  # the admin address. could've used our account.address direclty instead of using a proxy for the admin
        box_encoded_initializer_function,  # byte-encoded initializer function for the proxied contract
        {
            "from": account,
            "gas_limit": 1000000,
        },  # proxies have a difficulty figuring out the gas fees
    )
    print(f"Proxy deployed to {proxy}. It can now be upgraded to BoxV2")
    # let's point the original Box's ABI to be used in our proxy
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"{proxy_box.retrieve()=}")
