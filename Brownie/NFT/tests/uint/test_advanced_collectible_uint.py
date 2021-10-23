from brownie import accounts, network, config, AdvancedCollectible
import pytest
from scripts.advanced_collectible.deploy_nft import deploy_advanced_collectible, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_create_advanced_collectible():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    # Act
    advanced_collectible = deploy_advanced_collectible()
    # Assert
    assert advanced_collectible.tokenCounter() == 1
