// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract SimpleStorage {
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function storeFavoriteNumber(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieveFavoriteNumber() public view returns (uint256) {
        return favoriteNumber;
    }

    // Datatype string is an Array of Bytes so it has to be declared how it will be persist
    // Keyword memory: Data will only be stored during the Execution of the Function
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
