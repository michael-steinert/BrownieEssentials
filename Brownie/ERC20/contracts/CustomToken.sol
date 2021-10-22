// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract CustomToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("CustomToken", "CT") {
        _mint(msg.sender, initialSupply);
    }
}