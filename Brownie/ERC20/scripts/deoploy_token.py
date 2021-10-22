from brownie import accounts, config, network, CustomToken
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

initial_supply = Web3.toWei(42, "ether")

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    account = get_account()
    custom_token = CustomToken.deploy(initial_supply, {"from": account})
    print(f"{custom_token.name()} was deployed")
