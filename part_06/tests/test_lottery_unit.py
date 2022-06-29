from brownie import accounts, Lottery, network, config, exceptions
from scripts.deploy_lottery import deploy_lottery, get_account, fund_contract_with_link
from web3 import Web3
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract


def skip_test_if_not_local_env():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


def test_get_entrance_fee():
    skip_test_if_not_local_env()

    # GIVEN
    lottery = deploy_lottery()

    # WHEN

    # 50 / 2000 = 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()

    # THEN
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unles_started():
    skip_test_if_not_local_env()

    # GIVEN
    lottery = deploy_lottery()
    account = get_account()

    # WHEN / THEN
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": lottery.getEntranceFee()})


def test_cant_start_lottery_unless_owner():
    skip_test_if_not_local_env()

    # ARRANGE
    lottery = deploy_lottery()
    non_owner_account = get_account(1)

    # ACT/ASSERT
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.startLottery({"from": non_owner_account})


def test_can_start_lottery():
    skip_test_if_not_local_env()

    # ARRANGE
    lottery = deploy_lottery()
    owner_account = get_account()

    # ACT
    lottery.startLottery({"from": owner_account})

    # ASSERT
    assert lottery.lottery_state() == 0


def test_can_enter_lottery():
    skip_test_if_not_local_env()

    # ARRANGE
    lottery = deploy_lottery()
    owner_account = get_account()
    lottery.startLottery({"from": owner_account})

    # ACT
    lottery.enter({"from": owner_account, "value": lottery.getEntranceFee()})

    # ASSERT
    assert lottery.players(0) == owner_account.address


def test_can_end_lottery():
    skip_test_if_not_local_env()

    # ARRANGE
    lottery = deploy_lottery()
    owner_account = get_account()
    lottery.startLottery({"from": owner_account})
    lottery.enter({"from": owner_account, "value": lottery.getEntranceFee()})
    fund_contract_with_link(lottery.address)

    # ACT
    lottery.endLottery()

    # ASSERT
    assert lottery.lottery_state() == 2


def test_winner_is_picked_correctly():
    # ARRANGE
    skip_test_if_not_local_env()

    RANDOM_NUM: int = 777

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_contract_with_link(lottery)
    # read event off of the blockchain
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, RANDOM_NUM, lottery.address, {"from": account}
    )
    starting_balance_of_account: int = account.balance()
    balance_of_lottery = lottery.balance()
    assert lottery.recentWinner() == get_account()
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
