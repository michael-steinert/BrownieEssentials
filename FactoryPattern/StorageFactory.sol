// SPDX-License_Identifier: MIT
pragma solidity 0.8.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function simpleStorageStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // To interact with other Smart Contracts their Address and ABI are necessary
        // The ABI tells Solidity and other Programming Languages how it can interact with another Smart Contract
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).storeFavoriteNumber(_simpleStorageNumber);
    }

    function simpleStorageRetrieve(uint256 _simpleStorageIndex) public view returns (uint256) {
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieveFavoriteNumber();
    }
}
