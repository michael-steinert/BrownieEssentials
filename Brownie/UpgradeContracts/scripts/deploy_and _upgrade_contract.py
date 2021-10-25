from brownie import accounts, network, config, Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy, Contract
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]


# Arguments: encode_function_data(box.store, 42, 1, 2)
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


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
    print(f"Deploying to Network {network.show_active()}")
    box = Box.deploy({"from": account}, publish_source=True)
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    # Encoding the Initializer Function that is once call when the Contract is deployed
    initializer = (box.storeValue, 42)
    box_encoded_initializer_function = encode_function_data()

    # constructor(address _logic, address admin_, bytes memory _data)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True
    )
    print(f"Proxy deployed to {proxy} - now it is possible to upgrade Contracts")
    # Assigning the Box ABI to the Proxy Address - so the Proxy can delegate all its Call to the Box Contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # Calling Box Contract Functions on Proxy Contract - it contains the most recent deployed Implementation of the Implementation contract
    proxy_box.storeValue(42, {"from": account})
    print(proxy_box.retrieveValue())

    # Upgrading Implementation Contract
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)
    upgrading_transaction = None
    if proxy_admin:
        if initializer:
            encoded_function_call = encode_function_data(initializer)
            upgrading_transaction = proxy_admin.upgradeAndCall(
                proxy.address,
                box_v2.address,
                encoded_function_call,
                {"from": account}
            )
        else:
            upgrading_transaction = proxy_admin.upgrade(
                proxy.address,
                box_v2.address,
                {"from": account}
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer)
            upgrading_transaction = proxy.upgradeToAndCall(
                box_v2.address,
                encoded_function_call,
                {"from": account}
            )
        else:
            upgrading_transaction = proxy.upgradeTo(
                box_v2.address,
                {"from": account}
            )
    upgrading_transaction.wait(1)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # Calling BoxV2 Contract Functions on Proxy Contract - it contains the most recent deployed Implementation of the Implementation contract
    # The State of the Box Contract stayed in the Proxy Contract so the Value is 42
    print(proxy_box.retrieveValue())
    proxy_box.incrementValue({"from": account})
    print(proxy_box.retrieveValue())
