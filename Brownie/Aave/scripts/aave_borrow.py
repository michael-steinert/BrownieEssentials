from brownie import accounts, network, config, LotteryContract, MockV3Aggregator, VRFCoordinatorMock, LinkToken, \
    Contract, interface
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork"]


def get_weth(account, weth_erc20_address):
    weth = interface.IWeth(weth_erc20_address)
    # Deposit ETH to get wETH
    depositing_transaction = weth.deposit({"from": account, "value": Web3.toWei(0.1, "ether")})
    depositing_transaction.wait(1)
    return weth


def get_lending_pool():
    # LendingPoolAddressesProvider registers Addresses of the Protocol for a particular Market
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address):
    erc20 = interface.IERC20(erc20_address)
    approving_transaction = erc20.approve(spender, amount, {"from": get_account()})
    approving_transaction.wait(1)
    return approving_transaction


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_borrowable_data(lending_pool, account):
    # Returns the User Account Data across all the Reserves - function getUserAccountData(address user)
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor
    ) = lending_pool.getUserAccountData(account.address)
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    print(f"{total_collateral_eth} worth of ETH deposited")
    print(f"{total_debt_eth} worth of ETH borrowed")
    print(f"{available_borrow_eth} worth of ETH can be borrowed")
    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    # Answer for latest Price is in Tuple at Index 1
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    return float(Web3.fromWei(latest_price, "ether"))

def repay_all_borrowed_assets(amount, lending_pool, account):
    dai_address = config["networks"][network.show_active()]["dai_token"]
    approving_transaction = approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool.address,
        dai_address,
        account
    )
    # Repaying all Assets from Aave - function repay(address asset, uint256 amount, uint256 rateMode, address onBehalfOf)
    repaying_transaction = lending_pool(dai_address, amount, 1, account.address, {"from": account})
    # Waiting until one Block Confirmation
    repaying_transaction.wait(1)

def main():
    account = get_account()
    weth_erc20_address = config["networks"][network.show_active()]["weth_token"]
    # Swapping ETH to wETH - Wrapped Ether (wETH) is an ERC20 Token of ETH in the Aave Ecosystem to easily interact with other Tokens
    weth = get_weth(account, weth_erc20_address)
    lending_pool = get_lending_pool()
    # ERC20 need to approve Permission if someone want to work with it - Approve sending out ERC20 Tokens
    amount = Web3.toWei(0.1, "ether")
    approving_transaction = approve_erc20(amount, lending_pool.address, weth_erc20_address, account)
    # Deposit into Aave - function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)
    depositing_transaction = lending_pool.deposit(weth_erc20_address, amount, account.address, 0, {"from": account})
    # Waiting for one Block Confirmation
    depositing_transaction.wait(1)
    (available_borrow_eth, total_debt_eth) = get_borrowable_data(lending_pool, account.address)
    # Getting DAI Conversion Rate
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    # Calculating Amount of DAI to borrow
    # Multiply by Factor 0.94 to make sure that the Health Factor is above 1
    # Borrowable Ether -> Borrowable DAI * 94%
    amount_dai_to_borrow = (1 / dai_eth_price) * (available_borrow_eth * 0.94)
    # Borrow DAI from Aave - function borrow(address asset, uint256 amount, uint256 interestRateMode, uint16 referralCode, address onBehalfOf)
    dai_address = ["networks"][network.show_active()]["dai_token"]
    borrowing_transaction = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account}
    )
    # Waiting until one Block Confirmation
    borrowing_transaction.wait(1)
