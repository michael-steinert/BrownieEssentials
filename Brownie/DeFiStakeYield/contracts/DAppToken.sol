// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DAppToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("DApp Token", "DAPP") {
        _mint(msg.sender, 42 * 10 ** 18);
    }
}