// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Box {
    uint256 private value;

    event ValueChanged(uint256 newValue);

    // Proxy Contracts do not have a Constructor instead they have an Initializer Function which is run as the Contract is deployed
    function storeValue(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function retrieveValue() public view returns (uint256) {
        return value;
    }
}
