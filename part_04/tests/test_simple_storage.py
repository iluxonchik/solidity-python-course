from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    init_value = simple_storage.retrieve()
    expected_init_value = 0
    # Assert
    assert init_value == expected_init_value


def test_updating_storage():
    # Arrange
    account = accounts[0]

    # Act
    expected_value_after_store: int = 15
    simple_storage = SimpleStorage.deploy({"from": account})
    simple_storage.store(expected_value_after_store, {"from": account})

    # Assert
    result: int = simple_storage.retrieve()
    assert result == expected_value_after_store
