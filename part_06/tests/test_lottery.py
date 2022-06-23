from brownie import accounts, Lottery, network, config


def test_get_entrance_fee():
    account = accounts[0]
    lottery: Lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    entrance_fee = lottery.getEntranceFee()
