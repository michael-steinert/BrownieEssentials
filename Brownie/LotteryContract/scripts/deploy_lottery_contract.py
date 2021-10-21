from brownie import accounts, network, config, LotteryContract, MockV3Aggregator, VRFCoordinatorMock, LinkToken, Contract, interface
from web3 import Web3
import time

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]


def deploy_lottery_contract():
    account = get_account()

    # Deploy V3Aggregator
    # Grab Contract Addresses from Brownie Config if their are defined, otherwise deploy Mock Versions of that Contracts
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(MockV3Aggregator) <= 0:
            # Constructor(uint8 _decimals,int256 _initialAnswer)
            MockV3Aggregator.deploy(8, Web3.toWei(42, "ether"), {"from": account})
            # Getting the frequently deployed MockV3Aggregator
        price_feed = MockV3Aggregator[-1]
    else:
        price_feed_address = ["networks"][network.show_active()]["eth_usd_price_feed"]
        price_feed = Contract.from_abi(MockV3Aggregator._name, price_feed_address, MockV3Aggregator.abi)

    # Deploy LinkToken
    # Grab Contract Addresses from Brownie Config if their are defined, otherwise deploy Mock Versions of that Contracts
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(LinkToken) <= 0:
            LinkToken.deploy({"from": account})
        # Getting the frequently deployed LinkToken
        link_token = LinkToken[-1]
    else:
        link_token_address = ["networks"][network.show_active()]["link_token"]
        link_token = Contract.from_abi(LinkToken._name, link_token_address, LinkToken.abi)

    # Deploy VRFCoordinator
    # Grab Contract Addresses from Brownie Config if their are defined, otherwise deploy Mock Versions of that Contracts
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(VRFCoordinatorMock) <= 0:
            VRFCoordinatorMock.deploy(link_token.address, {"from": account})
        # Getting the frequently deployed VRFCoordinator
        vrf_coordinator = VRFCoordinatorMock[-1]
    else:
        vrf_coordinator_address = ["networks"][network.show_active()]["vrf_coordinator"]
        vrf_coordinator = Contract.from_abi(VRFCoordinatorMock._name, vrf_coordinator_address, VRFCoordinatorMock.abi)

    lottery_contract = LotteryContract.deploy(
        price_feed.address,
        vrf_coordinator.address,
        link_token.address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=["networks"][network.show_active()]["verify"]
    )
    return lottery_contract


def start_lottery():
    account = get_account()
    # Get frequently deployed Lottery Contract
    lottery_contract = LotteryContract[-1]
    starting_transaction = lottery_contract.startLottery({"from": account})
    # Waiting until the last Transaction finished
    starting_transaction.wait(1)
    print("Lottery is started")


def enter_lottery():
    account = get_account()
    # Get frequently deployed Lottery Contract
    lottery_contract = LotteryContract[-1]
    entrance_fee = lottery_contract.getEntranceFee()
    entering_transaction = lottery_contract.enterLottery({"from": account, "value": entrance_fee})
    entering_transaction.wait(1)
    print("Entered Lottery")


def end_lottery():
    account = get_account()
    # Get frequently deployed Lottery Contract
    lottery_contract = LotteryContract[-1]
    # First Contract has to be funded with 0.1 Link Token
    link_token = LinkToken[-1]
    funding_contract_with_link = link_token.transfer(lottery_contract.address, Web3.toWei(0.1, "ether"), {"from": account})
    # Alternative using Interfaces:
    # interface.LinkTokenInterface(link_token).transfer(lottery_contract.address, Web3.toWei(0.1, "ether"), {"from": account})
    funding_contract_with_link.wait(1)
    # Second end Lottery
    ending_transaction = lottery_contract.endLottery({"from": account})
    ending_transaction.wait(1)
    # Waiting 60 Seconds until the Chainlink Node responses the random Number
    time.sleep(60)
    print(f"{lottery_contract.recentWinner()} is the Winner")


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_lottery_contract()
    start_lottery()
    enter_lottery()
    end_lottery()
