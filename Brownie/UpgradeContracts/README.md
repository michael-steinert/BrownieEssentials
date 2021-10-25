# Upgrade Smart Contracts with the Proxy Pattern

* The Core Functionality of the  Proxy Pattern will be the same: it forwards all Messages it receives to the current Implementation of the Implementation Contract
* The Proxy Pattern is using the Methode delegatecall() - It forwards the current Message to the Implementation, sending it the exact same Data Parameter it received
* The Forwarding Logic in placed in the Fallback Function - this allows to forward any Call into the Proxy
* The Proxy also needs its own Meta-Functionality, as it needs to be upgradeable - So Functions like implementation() and proxyOwner() will not be forwarded, given that they exist and the Fallback Function is not executed
* delegatecall() is a special Variant of a Message Call
* delegatecall() is identical to a Message Call apart from the Fact that the Code ath the Target Address is executed in the Context of the calling Contract and msg.sender and msg.value do not change their Values
* For Example: Contract A is calling (delegatecalling) the Contract B - the Logic of Contract B is executed in the Context of Contract A

<p align="center">
    <img src="https://user-images.githubusercontent.com/29623199/138606154-4643a341-b755-47cf-80b1-2464e9c25126.JPG" alt="Delegatecall Example" width="90%"/>
</P>

* One Proxy Contract can has the same Address forever and only delegate the Calls to the specific Implementation (Contract)
* On the Proxy Contract can everytime a new Implementation (Address of specific Contract) been updated
* Proxy Pattern Terminology:
    * The __Implementation Contract__: Is the Contract which has all Code of a specific Protocol - When it is upgraded,
      a new Implementation of these Contract is launched
    * The __Proxy Contract__: Is the Contract which points to which Implementation is the correct one, and routes all
      Function Calls to that Contract
    * The __User__: The Users make calls to the Proxy Contract
    * The __Admin__: The Admin is the User (or Group of Users / Voters) who upgrade the Proxy Contract to points the new
      Implemenation Contract
* The Proxy Pattern allows deploying new Logic and keeps the old State of the Contract

## Transparent Proxy Pattern

* Admins can not call Implementation Functions of the Implementation Contract - only Users can it
* Admins can only call Admin Functions - Admin Function are Functions that govern the Upgrades of the Proxy Contract
* So a Function Selector Clash is prevented

## Universal Upgradeable Proxy Pattern

* Admin-only Upgrade Functions are in the Implementation Contract instead of the Proxy Contract
* So Gas can be saved

## Diamond tProxy Pattern

* Big Smart Contracts can be split into many Smart Contract if the maximum Size is reached
* So individual Functions can be changed
