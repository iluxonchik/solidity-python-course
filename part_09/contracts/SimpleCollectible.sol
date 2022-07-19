// SPDX-Licence-Idenitfier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("Dawg", "DOG") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        // an ERC-721 NFT is just assigining a tokenId to an address
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter += 1;
        return newTokenId;
    }
}
