pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is Ownable {
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    // address vs address payable:
    //     * you can call .transfer() and .send() on a payable address, but not on an address
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
    }

    function enter() public payable {
        // $50 minimum
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not open");
        require(msg.value >= getEntranceFee(), "Not enough Ether");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**18; // 18 decimals

        // solidity doesn't work with decinmals, so we need to do some convertions
        // https://ethereum.stackexchange.com/questions/35150/how-to-store-a-float-or-decimal-in-a-contract

        // 1 either = 10 ** 18 wei, i.e., 1 ether in wei has 18 decimal places
        // https://docs.ethers.io/v5/api/utils/display-logic/#:~:text=A%20Unit%20can%20be%20specified,bitcoin%20represents%20108%20satoshi)
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Can only OPEN a CLOSED lottery."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }
}