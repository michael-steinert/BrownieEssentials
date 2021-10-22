from brownie import accounts, network, config, exceptions, LinkToken, VRFCoordinatorMock
from web3 import Web3
from scripts.deploy_lottery_contract import deploy_lottery_contract, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    # Act - When
    # 42 USD (Minimum USD) / 2000 USD (Ether) = 0.021
    expected_entrance_fee = Web3.toWei(0.021, "ether")
    entrance_fee = lottery_contract.getEntraceFee()
    # Assert - Then
    assert expected_entrance_fee == entrance_fee


def test_can_not_enter_lottery_unless_stated():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    # Act - When
    # Assert - Then
    with pytest.raises(exceptions.VirtualMachineError):
        lottery_contract.enterLottery({"from": get_account(), "value": lottery_contract.getEntraceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    account = get_account()
    lottery_contract.startLottery({"from": account})
    # Act - When
    lottery_contract.enterLottery({"from": account, "value": lottery_contract.getEntranceFee()})
    # Assert - Then
    assert lottery_contract.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enterLottery({"from": account, "value": lottery_contract.getEntranceFee()})
    # Act - When
    # Lottery Contract has to be funded with Link for Chainlink Node - random Number
    link_token = LinkToken[-1]
    link_token.transfer(lottery_contract.address, Web3.toWei(0.1, "ether"), {"from": account})
    lottery_contract.endLottery({"from": account})
    # Assert - Then
    assert lottery_contract.lotteryState == 2  # 2 corresponds to LotteryState.CLOSED


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange - Given
    lottery_contract = deploy_lottery_contract()
    account = get_account()
    lottery_contract.startLottery({"from": account})
    lottery_contract.enterLottery({"from": account, "value": lottery_contract.getEntranceFee()})
    # Creating different Player
    lottery_contract.enterLottery({"from": get_account(index=1), "value": lottery_contract.getEntranceFee()})
    lottery_contract.enterLottery({"from": get_account(index=2), "value": lottery_contract.getEntranceFee()})
    # Lottery Contract has to be funded with Link for Chainlink Node - random Number
    link_token = LinkToken[-1]
    link_token.transfer(lottery_contract.address, Web3.toWei(0.1, "ether"), {"from": account})
    # Act - When
    ending_transaction = lottery_contract.endLottery({"from": account})
    request_id = ending_transaction.events["RandomnessRequested"]["requestId"]
    # Get frequently deployed VRF Coordinator
    vrf_coordinator = VRFCoordinatorMock[-1]
    static_random_number = 42
    vrf_coordinator.callBackWithRandomness(request_id, static_random_number, lottery_contract.address,
                                           {"from": account})
    # 3 Player and random Number 42 => 42 % 3 = 0 => Winner is first Player
    winner = get_account(index=0)
    starting_balance = winner.balance()
    lottery_balance = lottery_contract.balance()
    # Assert - Then
    assert lottery_contract.recentWinner() == winner
    assert lottery_contract.balance() == 0
    assert winner.balance() == starting_balance + lottery_balance
