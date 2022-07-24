from brownie import network, AdvancedCollectible
from scripts.utils import get_breed, get_account, OPENSEA_TESTNET_FORMAT

DOG_METADATA_CACHE: dict = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"On the {network.show_active()} network")
    advanced_collectible = AdvancedCollectible[-1]
    num_of_collectibles: int = advanced_collectible.tokenCounter()
    print(f"You have {num_of_collectibles} tokenIds")
    for token_id in range(num_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not advanced_collectible.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id=}")
        set_tokenURI(
            token_id,
            advanced_collectible,
            DOG_METADATA_CACHE[breed],
        )


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"You can view your NFT at {OPENSEA_TESTNET_FORMAT.format(nft_contract.address, token_id)}"
    )
