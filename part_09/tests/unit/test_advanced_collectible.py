from brownie import network, AdvancedCollectible
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # ARRANGE
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Not running on a local blockchain environment")

    # ACT

    # we are emitting an event on the creation transaction, and that event contains the request ID
    # we are able to read the event emitted in a transaction from the transaction object
    advanced_collectible, creating_tx = deploy_and_create()
    request_id = creating_tx.events["requestedCollectible"]["requestId"]
    random_number: int = 1992
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, random_number, advanced_collectible.address, {"from": get_account()}
    )

    # ASSERT
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
