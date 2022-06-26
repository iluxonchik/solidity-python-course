pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    modifier openLottery() {
        require(lottery_state == LOTTERY_STATE.OPEN, "Lottery isn't OPEN");
        _;
    }

    modifier calculatingWinner() {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lotery isn't CALCULATING_WINNER"
        );
        _;
    }
    uint256 public fee;
    bytes32 public keyhash;

    // address vs address payable:
    //     * you can call .transfer() and .send() on a payable address, but not on an address
    address payable[] public players;
    address payable public recentWinner;
    uint256 recentRandomNumber;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    LOTTERY_STATE public lottery_state;

    constructor(
        address _priceFeedAddress,
        address _vrfcoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfcoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
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

    // intersting explanation on how multiple modifiers would work:
    //   https://ethereum.stackexchange.com/questions/29608/whats-the-order-of-execution-for-multiple-function-modifiers
    function endLottery() public onlyOwner openLottery {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    // After we request a random number from a Chanlink Node, we will need to wait for that node to callback a function
    // on our contract and return that random number. It doesn't happen straight away.
    // The ChainLink node is calling the VRFCoodinator, and the VRFCoordinator will call fulfillRandomnes().
    // NOTE that we made fulfillRandomness internal, because we don't want to have anyone else but the VRFCoordinator calling that function.
    // fulfillRandomness is called in rawFulfillRandomness, WHICH HAS A require() THAT ONLY ALLOWS THE VRFCOORDINATOR to call that it. That rawFulfillRequest()
    // public function, after ensuring that it's being called by a VRFCoordinator, calls this internal funciton. Sicne we are inheriting from VRFConsumerBase
    // we alrady have that function and just need to override it, and the VRFCoordinator is aware of it too, because it's in its class.
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
        calculatingWinner
    {
        require(_randomness > 0, "random not found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentRandomNumber = _randomness;
        recentWinner.transfer(address(this).balance);

        // rest lottery state
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
