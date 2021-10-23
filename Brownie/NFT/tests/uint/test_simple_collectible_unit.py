from brownie import accounts, network, config, SimpleCollectible
import pytest
from scripts.simple_collectible.deploy_nft import deploy_and_create, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_create_simple_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    # Act
    simple_collectible = deploy_and_create()
    # Assert
    assert simple_collectible.ownerOf(0) == get_account()
