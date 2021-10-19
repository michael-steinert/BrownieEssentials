// SPDX-License_Identifier: MIT
pragma solidity >=0.6 <0.9.0;

// Imports are stored as NPM Packages
// A Library is deployed only once at a specific Address and their Code is reused
// Interfaces are compiled down to an ABI
// The ABI tells Solidity and other Programming Languages how it can interact with another Smart Contract
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundAddress {
    // Using Keyword: using A for B
    // Keyword "using" can be used to attach Library Functions (from the Library A) to any Type (B) in the Context of a Smart Contract
    // Using the Library SafeMathChainlink for all Variables of Type unit256 - prevent Overflow during arithmetic Operations
    using SafeMathChainLink for uint256;

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;
    address public owner;

    // A Modifier is sued to change the Behavior of a Function in a declarative Manner

    modifier onlyOwner {
        require(msg.sender == owner, "Only Owner of Smart Contract can use this Operation");
        // This Modifier will be checked before the Function is executed
        _;
    }

    modifier postFunctionModifier {
        // This Modifier will be checked after the Function is executed
        _;
        require(msg.sender == owner, "Only Owner of Smart Contract can use this Operation");
    }

    // Constructor is instantly invoked when the Smart Contact is deployed
    constructor() public {
        owner = msg.sender;
    }

    function fundContract() public payable {
        uint256 minimumUsd = 42 * 1 ether;
        // If Transaction is reverted the User get his Value and Parts of the unused Gas back
        require(getConversionRate(msg.value) >= minimumUsd, "At least 42USD are necessary");
        // msg.sender: Sender of the Transaction
        // msg.value: Value that was sent by Transaction
        addressToAmountFunded[msg.sender] += msg.value;
        // Push every Funder to the Funders-Array - so there is an Overview of all Funders - Funders can be redundant
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        // Address from Price Feed Contract in Chainlink Docs: https://docs.chain.link/docs/ethereum-addresses/
        // Calling the Price Feed Smart Contract with it Address on the Network Kovan
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        // Calling another Contract from Chainlink to get the Aggregator Version
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // Address from Price Feed Contract in Chainlink Docs: https://docs.chain.link/docs/ethereum-addresses/
        // Calling the Price Feed Smart Contract with it Address on the Network Kovan
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
        // Calling another Contract from Chainlink - it returns the following Tuple: (roundId, answer, startedAt, updatedAt,answeredInRound)
        // Tuple: A List of Objects of potentially different Types whose Number is a Constant at Compile-Time
        // Calling another Contract from Chainlink to get the Price feed for ETH / USD
        (,int256 answer,,,) = priceFeed.latestRoundData();
        // Type Casting from int256 to uint256
        return uint256(answer);
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 = ethPrice = getPrice();
        uint256 ethAmountInUsd = (getPrice * ethAmount) / 1 ether;
        return ethAmountInUsd;
    }

    function withdrawFunds() payable onlyOwner public {
        // Transferring all Balances of Smart Contract to msg.sender
        // Keyword "this": points to the current Smart Contract
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            // Resetting all funded Amount in Smart Contract after the Withdraw happened
            addressToAmountFunded[funder] = 0;
        }
        // Resetting all Funders
        funders = new address[](0);
    }
}
