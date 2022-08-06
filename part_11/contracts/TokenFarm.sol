// SPDX-License-Identifier: MIT
import "@openzeppelin/contracts/ownership/Ownable.sol";

contract TokenFarm is Ownable {
    // we need this contract to support the following functionality:
    // stakeTokens
    // unstakeTokens
    // issueTokens
    // addAllowedTokens
    // getEthValue

    address[] public allowedTokens;

    function stakeTokens(uint256 _amount, address _token) public {
        // which tokens can be staked?
        // how much can the tokens be staked?
        require(_amount > 0, "Amount must be more than 0");
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (uint256 index = 0; index < allowedTokens.length; index++) {
            if (allowedTokens[index] == _token) {
                return true;
            }
            return false;
        }
    }
}
