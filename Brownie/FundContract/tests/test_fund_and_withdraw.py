from brownie import network, config, accounts, exceptions, FundContract, MockV3Aggregator
from web3 import Web3
import pytest

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]


def test_can_fund_and_withdraw():
    account = get_account()
    fund_contract = deploy_fund_contract()
    entrance_fee = fund_contract.getEntranceFee()

    fund_transaction = fund_contract.fundContract({"from": account, "value": entrance_fee})
    # Waiting until Transaction is in a Block mined
    fund_transaction.wait(1)
    # Check that funded Amount is equal the saved Amount in Contract
    assert fund_contract.addressToAmountFunded(account.address) == entrance_fee

    withdraw_transaction = fund_contract.withdrawFunds({"from": account})
    # Waiting until Transaction is in a Block mined
    withdraw_transaction.wait(1)
    # Check that withdrew Amount is equal the saved Amount in Contract
    assert fund_contract.addressToAmountFunded(account.address) == 0

def test_only_owner_can_withdraw():
    if network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active in FORKED_LOCAL_ENVIRONMENTS:
        pytest.skip("Only for local Testing")
    fund_contract = deploy_fund_contract()
    not_owner = accounts.add()
    # Expected an Exception caused
    with pytest.raises(exceptions.VirtualMachineError):
        fund_contract.withdrawFunds({"from": not_owner})

def deploy_fund_contract():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active not in FORKED_LOCAL_ENVIRONMENTS:
        # Address from Price Feed Contract in Chainlink Docs: https://docs.chain.link/docs/ethereum-addresses/
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        print(f"The active Network is {network.show_active()}")
        if len(MockV3Aggregator) <= 0:
            #   constructor(uint8 _decimals,int256 _initialAnswer)
            MockV3Aggregator.deploy(8, Web3.toWei(42, "ether"), {"from": account})
        # Using the most frequently deployed MockV3Aggregator
        price_feed_address = MockV3Aggregator[-1].address

    fund_contract = FundContract.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    print(f"Contract deployed to {fund_contract.address}")
    return fund_contract


def get_account():
    if network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
