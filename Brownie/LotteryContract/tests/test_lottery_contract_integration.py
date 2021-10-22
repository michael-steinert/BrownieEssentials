from brownie import accounts, network, config, exceptions, LinkToken, VRFCoordinatorMock
from web3 import Web3
from scripts.deploy_lottery_contract import deploy_lottery_contract, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    account = get_account
    # Act - When
    lottery_contract.startLottery({"from": account})
    lottery_contract.enterLottery({"from": account, "value": lottery_contract.getEntranceFee()})
    # Lottery Contract has to be funded with Link for Chainlink Node - random Number
    link_token = LinkToken[-1]
    link_token.transfer(lottery_contract.address, Web3.toWei(0.1, "ether"), {"from": account})
    ending_transaction = lottery_contract.endLottery({"from": account})
    time.sleep(60)
    # Assert - Then
    assert lottery_contract.recentWinner() == account
    assert lottery_contract.balance() == 0
