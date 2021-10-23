from brownie import accounts, network, config, AdvancedCollectible, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]

sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def deploy_advanced_collectible():
    account = get_account()
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

    advanced_collectible = AdvancedCollectible.deploy(
        vrf_coordinator.address,
        link_token.address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account}
    )
    return advanced_collectible


def funding_contract_with_link(advanced_collectible):
    account = get_account()
    link_token = LinkToken[-1]
    funding_transaction = link_token.transfer(advanced_collectible.address, Web3.toWei(0.1, "ether"), {"from": account})
    # Waiting for one Block Confirmation
    funding_transaction.wait(1)


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
    advanced_collectible = deploy_advanced_collectible()
    # Fund Chainlink Node before using its Service
    funding_contract_with_link(advanced_collectible)
    creating_transaction = advanced_collectible.createCollectible({"from": account})
    # Waiting for one Block Confirmation
    creating_transaction.wait(1)
    print("New NFT has been created")
