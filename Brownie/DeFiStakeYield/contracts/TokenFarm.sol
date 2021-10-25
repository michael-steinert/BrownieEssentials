// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

/*
    A TokenFarm can:
    - stake Tokens
    - un-stake Tokens
    - issue Tokens (A Reword for those User which use the TokenFarm)
    - and allowed Tokens
    - Also get the underlying ETH Value of these staked Tokens by Price Feeds
*/
contract TokenFarm is Ownable {
    address[] public allowedTokensToStake;
    // Mapping: Token Address => Staker Address => Amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
    // Mapping: Staker Address => unique Token
    mapping(address => uint256) public uniqueTokensStaked;
    // Mapping of all Price Feed Contracts for each Token
    mapping(address => address) public tokenPriceFeedAddresses;
    // Array instead of Mapping because Looping on a Mapping is not possible
    address[] public stakers;
    // DAppToken which is used as Reward for Stakers
    IERC20 public dAppToken;

    constructor(address _dAppToken) public {
        dAppToken = IERC20(_dAppToken);
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowedToStake(_token), "Token is not allowed");
        // transfer() only works on the Address which owns the Tokens
        // transferFrom() works also if the Address does not own the Tokens - therefore the Tokens have to be first approved
        // The TokenFarm Contract does not own the Tokens so the transferFrom() is used
        // Getting the ABI from the ERC20 Token via the Interface and calling the transferFrom to transfer these Tokens to this contract
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        // Determine how many unique Tokens a User has - if one unique Token then the User is added to the Staker List
        updateUniqueTokensStaked(msg.sender, _token);
        // Mapping: Token Address => Staker Address => Amount: Add Amount to exists Amount of Staker
        stakingBalance[_token][msg.sender] = stakingBalance[_token][msg.sender] + _amount;
        // If this is the first Token of these User then add him to the Staker List
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function addAllowedTokenToStake(address _token) public onlyOwner {
        allowedTokensToStake.push(_token);
    }

    function tokenIsAllowedToStake(address _token) public returns (bool) {
        for (uint256 i = 0; i < allowedTokensToStake.length; i++) {
            if (allowedTokensToStake[i] == _token) {
                return true;
            }
        }
        return false;
    }

    function unStakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Stacking Balance can not be 0");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        // Reset the Staked Identifier
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;
        // Delete Staker from Staker List
        for (uint256 i = 0; i < stakers.length; i++) {
            if (stakers[i] == msg.sender) {
                delete stakers[i];
            }
        }
    }

    function issueTokens() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address recipient = stakers[i];
            // Sending Token Reward (DAppToken) to Staker based on their Total Value locked
            uint256 recipientTotalValue = getRecipientTotalValue(recipient);
            // Using transfer() because this Contract actually owns the Tokens
            dAppToken.transfer(recipient, recipientTotalValue);
        }
    }

    function getRecipientTotalValue(address _recipient) public view returns (uint256) {
        require(uniqueTokensStaked[_recipient] > 0, "User does not staked any Tokens");
        uint256 totalValue = 0;
        for (uint256 i = 0; i < allowedTokensToStake.length; i++) {
            totalValue = totalValue + getUserSingleTokenValue(_recipient, allowedTokensToStake[i]);
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token) public view returns (uint256) {
        // Using if-Check instead of require-Check because a require-Check would interrupt the Procedure
        if (uniqueTokensStaked[_user] <= 0) {
            return 0;
        }
        // Getting Value of Token then multiply it by the Staking Balance of this User
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return (stakingBalance[_token][_user] * price / (10 ** decimals));
    }

    function getTokenValue(address _token) public view returns (uint256, uint256) {
        // Using a Price feed from Chainlink
        address priceFeedAddress = tokenPriceFeedAddresses[_token];
        // Using the Price Feed Address in a V3 Aggregator to get the Price Feed
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        // (uint80 roundID, int price, uint startedAt, uint timeStamp, uint80 answeredInRound) = priceFeed.latestRoundData();
        (, int256 price, , ,) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function setPriceFeedAddresses(address _token, address _priceFeed) public onlyOwner {
        /*
           Mainnet: ETH / USD - 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419
           Kovan: ETH / USD	- 0x9326BFA02ADD2366b30bacB125260Af641031331
           Rinkeby: ETH / USD - 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        */
        tokenPriceFeedAddresses[_token] = _priceFeed;
    }

    // Keyword internal: Only this Contract can call this Function
    function updateUniqueTokensStaked(address _user, address _token) internal {
        // If User has no Amount in this Token staked then he is added to the Staker List
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }
}

