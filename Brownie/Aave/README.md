# Aave
* Aave is a decentralised non-custodial Liquidity Protocol where Users can participate as Depositors or Borrowers
* Depositors provide Liquidity to the Market to earn a passive Income
* Borrowers are able to borrow in an over-collateralized (perpetually) or under-collateralized (one-block liquidity) Manner

## Lending Pool
* The LendingPool Contract is the Main Contract of the Protocol
* It exposes all the user-oriented Actions (deposit, withdraw, borrow, repay, etc.) that can be invoked using either Solidity or Web3 Libraries
* The LendingPoolAddressesProvider registers Addresses of the Protocol for a particular Market
* 