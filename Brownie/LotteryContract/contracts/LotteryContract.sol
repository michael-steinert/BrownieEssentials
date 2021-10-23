// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract LotteryContract is Ownable, VRFConsumerBase {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LotteryState {OPEN, CLOSED, CALCULATING_WINNER}
    LotteryState public lotteryState;
    event RandomnessRequested(bytes32 requestId);
    event LotteryClosed(address _winner, uint _amount);
    // Fee for VRF Chainlink Node to pay for its Service
    uint256 public fee;
    // Address to uniquely identify the Chainlink Node
    bytes32 public keyHash;

    constructor(address _priceFeed, address _vrfCoordinator, address _link, uint256 _fee, bytes32 _keyHash) public VRFConsumerBase(_vrfCoordinator, _link) {
        // Minimum 42$ as Entry fee
        usdEntryFee = 42 * 1 ether;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeed);
        lotteryState = LotteryState.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enterLottery() public payable {
        require(lotteryState == LotteryState.OPEN, "Lottery is not open");
        require(msg.value >= getEntranceFee(), "Not enough ETH to enter the Lottery");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (,int price,,,) = ethUsdPriceFeed.latestRoundData();
        // Price Feed has 8 Decimals so 10 Decimals left
        uint256 convertedPrice = uint256(price) * 10 ** 10;
        uint256 costToEnterLottery = (usdEntryFee * 1 ether) / convertedPrice;
        return costToEnterLottery;
    }

    function startLottery() public onlyOwner {
        require(lotteryState == LotteryState.CLOSED, "Can not start a new Lottery");
        lotteryState = LotteryState.OPEN;
    }

    function endLottery() public onlyOwner {
        /*
        // Using globally available Variable to generate Pseudo Randomness
        uint(keccak256( // Hashing- Algorithm is always the same so it is not random
                abi.encodePacked(
                    nonce, // Nonce is predictable, cause is correspond to the Transaction Number
                        msg.sender, // Sender - Address is predictable
                        block.difficulty, // Difficulty can be manipulated by the Miners
                        block.timestamp // Timestamp is predictable cause each Block has about the same Time
                )
            )
        ) % players.length;
        */
        lotteryState = LotteryState.CALCULATING_WINNER;
        // Using Chainlink VRF (Verifiable Random Function) is a provably-fair and verifiable Source of Randomness
        /*
        The Method follows the Request-Response Architecture:
        - First Transaction requests the random Number from the Chainlink Oracle - requestRandomness()
        - A second Callback Transaction responses the random Number to the Contract - fulfillRandomness()
        */
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RandomnessRequested(requestId);
    }

    // Only the Contract can call this Method so it is random - internal
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lotteryState == LotteryState.CALCULATING_WINNER, "Lottery is still running");
        require(_randomness > 0, "Random Number not found");
        uint indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        emit LotteryClosed(recentWinner, address(this).balance);
        // Resting all Player
        players = new address payable[](0);
        lotteryState = LotteryState.CLOSED;
    }
}
