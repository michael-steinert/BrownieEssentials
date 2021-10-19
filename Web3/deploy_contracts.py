import json
import os

from dotenv import load_dotenv
from web3 import Web3
# Python Wrapper and Version Management Tool for the solc Solidity Compiler
from solcx import compile_standard, install_solc

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Installing Solidity Compiler Version 0.8.0
install_solc("0.8.0")

# Compile Smart Contract
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SimpleStorage.sol":
                {
                    "content": simple_storage_file
                }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Getting Bytecode from compiled File
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"]["object"]

# Getting ABI from compiled File
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# Connecting to Ganache - local Blockchain
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337

eth_address = os.getenv("ETH_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Creating Smart Contract
simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Nonce in a Wallet - Transaction: The Account Nonce track the Number of Transactions made
nonce = w3.eth.get_transaction_count(eth_address)

# 1. Build Contract Deploy Transaction
transaction = simple_storage.constructor().buildTransaction({
    "chainId": chain_id,
    "from": eth_address,
    "nonce": nonce
})

# 2. Sign the Transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send the Transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

# Waiting for Block Confirmation - Application stops until a new Block is mined
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

# Interacting with deployed Smart Contract
# Interacting as Call: Simulate making the Call and getting a Return Value - No State Change of Blockchain
# Interacting as Transact: State Change of Blockchain
deployed_contract = w3.eth.contract(address=transaction_receipt.contractAddress, abi=abi)

# Print initial Value of FavoriteNumber
print(deployed_contract.functions.retrieveFavoriteNumber().call())

# Set Value of FavoriteNumber
store_transaction = deployed_contract.functions.storeFavoriteNumber(42).buildTransaction({
    "chainId": chain_id,
    "from": eth_address,
    # Nonce was used in initial Transaction to deploy the Smart Contract
    "nonce": nonce + 1
})
signed_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
store_transaction_hash = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(store_transaction_hash)

# Print new Value of FavoriteNumber
print(deployed_contract.functions.retrieveFavoriteNumber().call())
