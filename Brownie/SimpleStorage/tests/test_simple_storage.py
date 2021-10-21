from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange - Given
    account = accounts[0]
    # Act - When
    simple_storage = SimpleStorage.deploy({"from": account})
    initial_value = simple_storage.retrieveFavoriteNumber()
    # Assert - That
    assert (initial_value == 0)


def test_updating_storage():
    # Arrange - Given
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act - When
    simple_storage.storeFavoriteNumber(42)
    updated_value = simple_storage.retrieveFavoriteNumber()
    # Assert - Then
    assert (updated_value == 42)
