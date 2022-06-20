pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract Lottery {
    // address vs address payable:
    //     * you can call .transfer() and .send() on a payable address, but not on an address
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public payable {
        // $50 minimum
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        //
    }

    function startLottery() public {}
}
