from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    # Loading a random Account
    # account = accounts[0]

    # Loading a Custom Account
    # account = accounts.load("my-account")

    # Loading from Environment Variables
    # account = accounts.add(config["wallets"]["from_key"])

    account = get_account()

    # Deploy Smart Contract to a Blockchain
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)

    stored_value = simple_storage.retrieveFavoriteNumber()
    print(stored_value)

    transaction = simple_storage.storeFavoriteNumber(42, {"from": account})
    # Wait until Transaction is mined
    transaction.wait(1)

    new_stored_value = simple_storage.retrieveFavoriteNumber()
    print(new_stored_value)


def get_account():
    if (network.show_active == "development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
