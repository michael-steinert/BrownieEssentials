from brownie import network, accounts, config, FundContract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def deposit_contract():
    # Using the most frequently deployed FundContract
    fund_contract = FundContract[-1]
    account = get_account()
    entrance_fee = fund_contract.getEntranceFee()
    print(f"The current Entry Fee is {entrance_fee}")
    fund_contract.fundContract({"from": account, "value": entrance_fee})


def withdraw_contract():
    # Using the most frequently deployed FundContract
    fund_contract = FundContract[-1]
    account = get_account()
    fund_contract.withdrawFunds({"from": account})


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deposit_contract()
    withdraw_contract()
