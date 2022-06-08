// SPDX-License-Identifier: MIT

/*
    Smart contract that lets anyone depopst ETH into the contract
    Only the owner of hte contract can widthraw the deposited ETH
*/

pragma solidity >= 0.6.6 < 0.9.0;

// Get hte latest ETH/USD price from the Chanilink price feed
// these are NPM packages
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    // network: Kovan, aggregator: ETH/USD address
    address internal constant kovan_eth_usd_aggregator = 0x9326BFA02ADD2366b30bacB125260Af641031331;

    // mapping to store which address deposited how much ETH
    mapping(address => uint256) public addressToAmountFunded;
    // array of addresses that deposited ETH
    address[] public funders;
    // address of the owner (who deployed the contract)
    address public owner;

    // constructor() is called on the contract deploy. msg.sender contains the address
    // of the entity performing the contract call. on contract creation this entity will
    // be the one that created the contract, thus msg.sender in the constructor() 
    // will containd the address of the entity that created/owns the contract
    constructor() public {
        owner = msg.sender;
    }

    // get version of ChaninLink pricefeed
    function getVersion() public view returns(uint256) {
        // network: Kovan, aggregator: ETH/USD address
        AggregatorV3Interface priceFeed = AggregatorV3Interface(kovan_eth_usd_aggregator);
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        // network: Kovan, aggregator: ETH/USD address
        AggregatorV3Interface priceFeed = AggregatorV3Interface(kovan_eth_usd_aggregator);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        // ETH/USD rate in 18 digits. the returned value already has 8 zeroes, so we will add 10 more
        return uint256(answer * 10000000000);

    }

    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        // remove the 18 zeroes from the price
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    /*
        A function marked as "payable" can receive and/or send ETH. The amount of ETH received will go into the
        "value" field.
    */
    function fund() public payable {
        // WEI contain 18 zeroes, so let's convert to that format the USD too, so that we can then compare them
        uint256 minimumUSD = 2 * 10 ** 18;
        // if the donated amount is less than 2 USD, then revert
        require(getConversionRate(msg.value) >= minimumUSD, "A minimum of 50 USD is required");
        // if we reach this line, then the sent ETH amount was >= 50 USD
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    modifier onlyOwner {
        // asssert that the message sender is the owner of the contract, or revert
        require(msg.sender == owner);
        _;
        // "_" means run whatever the code is in the funciton after. you can also put it above the code in the modifier, and this way,
        // the code of the function that you are modifying will run before the code of the modifier.
        // this is very similar to a decorator in Python, or the decorator design pattern
    }

    function withdraw() payable onlyOwner public {
        // in Solidity v0.8.0 you must put payable(msg.sender)
        msg.sender.transfer(address(this).balance);

        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        // clear the funders array
        funders = new address[](0);

    }
}