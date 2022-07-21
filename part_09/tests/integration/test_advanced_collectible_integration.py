from brownie import network, AdvancedCollectible
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract, get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
import time


def test_can_create_advanced_collectible_integration():
    # ARRANGE
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test skipped since we are in a local blockchain environment")

    # ACT

    # we are emitting an event on the creation transaction, and that event contains the request ID
    # we are able to read the event emitted in a transaction from the transaction object
    advanced_collectible, creating_tx = deploy_and_create()
    time.sleep(60)

    # ASSERT
    assert advanced_collectible.tokenCounter() == 1
