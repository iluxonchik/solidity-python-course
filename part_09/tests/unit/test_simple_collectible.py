import pytest
from brownie import network
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy_and_create import deploy_and_create


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Not in a local environment")

    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()
