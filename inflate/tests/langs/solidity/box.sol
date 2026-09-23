pragma solidity ^0.8.0;

contract Box {
    function helper(uint value) internal pure returns (uint) {
        return value + 1;
    }

    function greet(uint value) internal pure returns (uint) {
        return helper(value) * 2;
    }

    function runner() public pure returns (uint) {
        return greet(3);
    }
}
