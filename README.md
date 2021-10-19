# Blockchain

- Blockchains are used to make Peer-to-Peer Transactions in a decentralized Network
- This Network is powered by Cryptography and allows People to engage in Censorship-resistant Finance in a decentralized Manner

## Characteristics of Blockchains

__Decentralized__:

- Decentralized Manner meaning there is no centralized Source that controls the Blockchain
- A decentralized Network is run by independent Users
- Full Replicas being run by independent and Sybil-resistant Node Operators, coming to Consensus about a Computation
- A Sybil Attack is an Attack on Peer-to-Peer Networks by creating false Identities - The Attack can be aimed at influencing Majority Voting and Network Organization
- Focused on Data Validation and Consensus about individual off-Chain Values to make them reliable enough to trigger Smart Contracts
- Node Operators are Security reviewed, can provide a proven Performance History and are high Quality and highly Sybil-resistant

__Transparency and Flexibly__:

- All Rules that are made in a Blockchain can be seen by everyone - everyone can see exactly the Rules and have to follow those Rules
- A Blockchain is pseudo-anonymous, so it is not possible to track Data - everyone can create different accounts and can interact with it in many Ways

__Speed and Efficiency__:
-Cause Blockchains are verified by a decentralized Collective so the Settlement and Withdrawal Period is fast and efficient

__Security and Immutability__:

- Blockchains can not be changed that means they can not be tampered or corrupted - this allows massive Security on Data
- As long as one Node in the Network is running the entire System is running - this makes Data safe and secure
- A Node is a single Instance in a decentralized Network

__Trust-less Agreements__

- Whatever the Code determines is the Output that is exactly what will happen every Time

- Smart Contracts allow Agreements without a Third-Party Intermediary or centralized governing Force
- A Smart Contract is a self-executing Set of Instructions that us executed without a Third-Party Intermediary
- The Terms of the Agreement are written in Code and automatically executed by the decentralized Blockchain Network

- The Ethereum Blockchain is deterministic - so all Things that happens were in the Blockchain this causes the Oracle Problem
- Oracle Problem: Smart Contracts need some Way to interact with the real World and get real Data and external outside the Blockchain Computation
- Oracles are Devices that bring Data into the Blockchain or execute some Type or external Computation
- For a Blockchain to remain decentralized, the Oracle must work in a decentralized Manner

- Centralized Oracles are a Point of Failure:
- ChainLink is a decentralized, modular Oracle Network that allows to bring Data into Smart Contracts and do external Computation

## Decentralized autonomous organization(DAO)
- A DAO is Organization that exists online tin Smart Contracts They have People who hold Governance Tokens to make Voting Decisions

## Gas
- Gas is a Unit of computational Measure
- The more Computation a Transaction uses the more Gas it has to pay
- Every Transaction that happens on-chain pays a Gas Fee to the Nodes for successfully included the Transaction into a Block
- The Amount of Gas used and how much the Transaction costs depends on how computationally expensive the Transaction is

- Gas: Measure of Computation Use
- Gas Price: how much it costs per Unit of Gas
- Gas Limit: Max Amount of Gas in a Transaction
- Transaction Fee: Gas used * Gas Price

- Gas Price is based off the Demand of the Blockchain
- The more People want to make Transactions, the higher the Gas Price, and therefore higher the Transaction Fees
- Because the Number of Transactions the Miner chose the Transactions with the highest Gas Price
- Because the Miners get the Transaction Fees if they successfully added the Transactions into a Block

# How a Blockchain works

* Hash is a unique, fixed-length String, meant ti identify a Piece of Data
* Hash Algorithm is a Function that computes Data into a unique Hash
* Mining ist the Process of Finding the Solution to the Blockchain Problem - for Example: The Problem can be to find a Hash that starts with four Zeros
* A Block is a List of Transactions (and Nonce, Previous Hash, Block-Number, Block-Hash, etc.) mined together
* Nonce is a Number used once to find the Solution to the Blockchain Problem

## Private Key
- The Private Key is only known to the Key-Holder, and it is used to sign Transactions

## Public Key
- The Public Key is derived from the private Key 
- The Address is derived from the public Key 
- The Public Key and Address can everybody know - so they are used to receiving Transactions and verify that a Transaction came from the Owner

## Digital Signature
- It is a One-Way Process in which a private Key ist used to sign a Transaction by hashing the private Key and the Transaction Data
- The Digital Signature is made of a Message and the Private Key using the Elliptic Curve Algorithm
- From the digital Signature it is not possible to derive the private Key

- Everyone can verify the digital Signature with the Message and the corresponding public Key - it has to be the same digital Signature:
- (Sign) private Key + Message = digital Signature = Message + public Key (Verify)

## Consensus
Consensus is the Mechanism which is used to agree on the State of a Blockchain

## Proof-of-Work
- Proof-of-Work: A single Node has to go through a very computationally expensive Process called Mining to figure out
  the correct Nonce for the Blockchain Problem
- The Block Time can be changed by the Difficulty of those Problems - The Block Time is the Time how long it takes between Blocks being published, and it is proportional to the Difficulty of those PProblems
- The Difficulty can be changed - this depends on the Number of Nodes in the Network - so fewer Nodes' means less computational Power so the Difficulty is set low
- PoW is sa verifiable Way to figure out who the Block Author is
- PoW is combined with the longest-Chain Rule (Nakamoto Consensus)
- The Longest-Chain Rule considers the longest Blockchain as the true Blockchain - The decentralized Network decides that whichever Blockchain has the Number of Blocks on it is going to be the Chain that is used
- The Longest-Chain Rule works well because every Block a Blockchain is behind it takes more and more Computation for it to come up
- Block Confirmation is the Number of additional Blocks that are added on after a specific Transaction went through in a Block
- In a PoW Network get the Miners the Transaction Fees if they added a Block
- In a PoW Network all Nodes are competing against each other to find the Nonce for the Blockchain Problem
- The first Node which finds the correct Nonce gets all Transactions Fees from the Block - the other Nodes do not get any Transaction Fees, so they have spent their computing Power for nothing
- The Node which find the correct Nonce get the Transactions Fees of the Block and a Block Reward
- The Transaction Fees are paid by whoever initialized the Transaction - it is the Gas that is used in these Transactions to pay for the computational Effort on the Network
- The Block Reward is given to these Nodes from the Protocol of the Blockchain itself - The Block Reward increases the circulating Amount of Cryptocurrency

## Proof-of-Stake
- Proof-of-Stake: A single Node puts up some Collateral (Cryptocurrency) that it is going to behave honestly in the
  Network - if the Node misbehaves it is going to be slashed or removed of its Collateral (Cryptocurrency)
- In a PoS Network get the Validators the Transaction Fees if they added a Block
- In PoS there is also a Transaction Fee in form of Gas - this si paid out to Validators
- Validator are validating other Nodes - A Validator is randomly chosen to propose the new Block and the other Validators will validate if that Validator (Node) has proposed the Block honestly
- To verify a Proposal it is very easy because of the Manner of Cryptography [Finding a Nonce is hard but verify those Nonce is easy]
- To chose randomly a Validator the Randomness Mechanism Randow is used - Randow is a decentralized autonomous Organisation that collectively chooses a random Number and which Node is going to run next as a Validator

## Sharding:
A shared Blockchain means that it is going to be Blockchain of Blockchains A Main Blockchain is going to coordinate all
Blockchains that hook it - So there are more Blockchain for User to make Transactions on Sharding allows to increase the
Number of Transaction on the first Layer (Base Blockchain)
Layer 1 refers to the base Layer Blockchain Implementation Layer2 refers an Application that is added on Top of a base
Blockchain

# Solidity

* Keyword memory: Data will only be stored during the Execution of the Function
* Keyword storage: Data will be persisted after the Execution of the Function
* keyword string: String is an Array of Bytes - so it is technical an Object so the Keyword memory or storage is used to for the Save Manner of this Object

# Ganache-CLI
|Command|Description|
|---|---|
|ganache-cli|Start a local Blockchain|
|ganache-cli -d|Run a local deterministic Blockchain with always the same Private Keys|