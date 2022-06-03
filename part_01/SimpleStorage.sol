// SPDX-License-Identifier: MIT


pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber;

    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    Person[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view functions read the state off of the blockchain and don't creaet a new
    // transaction
    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
