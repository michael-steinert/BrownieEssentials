// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BoxV2 {
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function storeValue(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function retrieveValue() public view returns (uint256) {
        return value;
    }

    function incrementValue() public {
        value++;
        emit ValueChanged(value);
    }
}
