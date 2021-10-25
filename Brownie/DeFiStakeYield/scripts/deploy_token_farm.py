from brownie import accounts, network, config, Contract, DAppToken, TokenFarm, MockV3Aggregator, MockDAI, MockWETH
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]


def deploy_token_farm():
    account = get_account()
    # Deploy DAppToken
    d_app_token = DAppToken.deploy({"from": account})
    # Deploy TokenFarm
    token_farm = TokenFarm.deploy(
        d_app_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )
    transferring_transaction = d_app_token.transfer(token_farm.address, d_app_token.totalSupply(), {"from": account})
    # Wait one Block Confirmation
    transferring_transaction.wait(1)
    # Allowing Token: dApp Token, wETH Token Faucet Token

    # Deploy MockWETH
    # Grab Contract Addresses from Brownie Config if their are defined, otherwise deploy Mock Versions of that Contracts
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(MockWETH) <= 0:
            MockWETH.deploy({"from": account})
        # Getting the frequently deployed MockWETH
        w_eth_token = MockWETH[-1]
    else:
        w_eth_token_address = ["networks"][network.show_active()]["w_eth_token"]
        w_eth_token = Contract.from_abi(MockWETH._name, w_eth_token_address, MockWETH.abi)

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
    # Getting Allowance for DApp Token
    adding_transaction = None
    adding_transaction = token_farm.addAllowedTokens(d_app_token.address,{"from": account})
    adding_transaction.wait(1)
    # Getting Allowance for wETH Token
    adding_transaction = token_farm.addAllowedTokens(w_eth_token.address,{"from": account})
    adding_transaction.wait(1)
    # Setting the Price Feed Address
    setting_transaction = token_farm.setPriceFeedAddresses(price_feed.address, {"from": account})
    setting_transaction.wait(1)

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_token_farm()
