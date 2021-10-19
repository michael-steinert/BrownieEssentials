// SPDX-License_Identifier: MIT
pragma solidity >=0.6 <0.9.0;

contract Overflow {
    // An Overflow is the Situation where the resulting Value of an arithmetic Operation, when executed on an unrestricted Integer, falls outside the Range of the Result Type
    // Since Solidity 0.8.0, all arithmetic Operations revert on Overflow by default, , thus making the use of these Libraries SafeMath from Openzeppelin unnecessary.
    // To obtain this Behaviour, an unchecked-Block can be used:
    function overflow() public view returns (uint8) {
        unchecked {
            uint8 maxUint8 = 255 + uint8(1);
            return maxUint8;
        }
    }
}
