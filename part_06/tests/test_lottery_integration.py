from brownie import network
from scripts.utils import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_contract_with_link,
)
from scripts.deploy_lottery import deploy_lottery
import pytest
from time import sleep


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("On a local network, skipping the integration test")
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_contract_with_link(lottery)
    lottery.endLottery({"from": account})
    sleep(60)
    assert lottery.balance() == 0
    assert lottery.recentWinner() == account
