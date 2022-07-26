from brownie import (
    Box,
    BoxV2,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    config,
    network,
)


def main():

    from scripts.utils import encode_function_data, get_account, upgrade

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
    tx = proxy_box.store(1, {"from": account})
    tx.wait(1)
    print(f"{proxy_box.retrieve()=}")

    # UPGRADE THE CONTRACT TO WHICH THE PROXY IS POINTING TO #
    print(f"Deploying BoxV2 to {network.show_active()}")
    box_v2 = BoxV2.deploy(
        {"from": account},
    )
    tx = upgrade(account, proxy, box_v2.address, proxy_admin)
    tx.wait(1)
    print("Proxy upgraded to BoxV2!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(f"Starting value: {proxy_box.retrieve()}")
    tx = proxy_box.increment({"from": account})
    tx.wait(1)
    print(f"Ending value: {proxy_box.retrieve()}")
