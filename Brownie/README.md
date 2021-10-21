# Python

## Creating a virtual Environment

```python
# Creating a virtual Environment
py -m pip install --user virtualenv
py -m venv env

# Activate virtual Environment
.\env\Scripts\activate

# Install Brownie
pip install eth-brownie

# Deactivate virtual Environment
deactivate
```

## Using Brownie

|Command|Description|
|---|---|
|brownie init|Initialize a new Brownie Project|
|brownie compile|Compile a Brownie Project|
|brownie run .\scripts\deploy_contracts.py|Run a Script inside a Brownie Project|
|brownie run .\scripts\deploy_contracts.py --network rinkeby|Run a Script inside a Brownie Project on the Network Rinkeby|
|brownie accounts new my-account|Add a Custom Account into a Brownie Project (A leading 0x has to be entered before the Private Key)|
|brownie accounts list|List all Custom Accounts from a Brownie Project|
|brownie accounts delete my-account|Delete a Custom Accounts from a Brownie Project|
|brownie test|Run all Tests from a Brownie Project|
|brownie test -k deploy_simple_storage|Run a selected Test from a Brownie Project|
|brownie test -pdb|Run all Tests from a Brownie Project and allow to check in a Python Debugger all failure Tests|
|brownie networks list|List all available Networks for those Brownie Project|
|brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=1337|Add a local Blockchain for those Brownie Project|
|brownie networks add development mainnet-fork cmd=ganache-cli host=http://127.0.0.1:7545 fork="https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID" accounts=10 mnemonic=brownie port=7545|Add a Frok from the Mainnet for those Brownie Project|
|brownie console|Open a Brownie Console to interact with all Resources from a Brownie Project|
